import re
import plivo
from plivo.exceptions import ValidationError

from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site

from celery import shared_task

from .words import (
    loose_maybe_words,
    exact_maybe_words,
    loose_no_words,
    exact_no_words,
    loose_yes_words,
    exact_yes_words,
)
from .models import MTRequest, MTSent
from apps.team.models import Player, Game, PlayerAttending, TeamMessage


def send_sms(phone, content, eta=None):
    if not eta:
        eta = timezone.now()
    print(phone, content, str(eta))

    player = Player.objects.get(phone_number=phone)

    content = content.format(first_name=player.first_name, last_name=player.last_name)
    mt_request = MTRequest.objects.create(phone_number=phone, content=content)
    _send_sms_to_portal.apply_async((phone, content, mt_request.pk), eta=eta)


@shared_task
def _send_sms_to_portal(phone, content, request_id):
    client = plivo.RestClient()

    try:
        response = client.messages.create(
            src="18159790956", dst=phone, text=content, url="{}/api/sms_dr_report/".format(get_current_site())
        )
        if response[0] in (200, 201, 202):
            MTSent.objects.create(
                phone_number=phone,
                content=content,
                request_id=request_id,
                aggregator_id=response[1].get("u'message_uuid"),
            )
    except ValidationError as err:
        print(err)


@shared_task
def process_mo(from_phone, to_phone, content):
    player = Player.objects.get(phone_number=from_phone)
    answer = None

    # Process and split MO sentence
    content = content.strip().lower()
    content = re.sub(r"[^\w\s]", "", content)
    content_split = re.split("\s+", content)

    # WIP natural language processing.  Will be improved in the future
    for word in content_split:
        for maybe_word in loose_maybe_words:
            if maybe_word in word:
                answer = "maybe"
                break
        for maybe_word in exact_maybe_words:
            if word == maybe_word:
                answer = "maybe"
                break
        for no_word in loose_no_words:
            if no_word in word:
                answer = "no"
                break
        for no_word in exact_no_words:
            if word == no_word:
                answer = "no"
                break
        for yes_word in loose_yes_words:
            if yes_word in word:
                answer = "yes"
                break
        for yes_word in exact_yes_words:
            if word == yes_word:
                answer = "yes"
                break

    # Process a few additional sentences (multi-word context)
    joined_content = " ".join(content)
    if "not sure" in joined_content or "ill try" in joined_content:
        answer = "maybe"

    # Get the last message sent to the player
    team_message = (
        TeamMessage.objects.filter(players=player, date_to_send__lt=timezone.now()).order_by("-date_to_send").first()
    )
    # Get the next game
    game = Game.objects.filter(date__gt=timezone.now(), team=team_message.team).order_by("date").first()

    # Create a playerattending or update the last instance
    PlayerAttending.objects.update_or_create(
        team=team_message.team, player=player, game=game, defaults={"going": answer}
    )
