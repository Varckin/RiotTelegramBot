from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import get_api_riot
import heroes
import variables

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Hello {message.chat.first_name}"
                         f"For get more info, enter /info")


@router.message(Command("player"))
async def cmd_player(message: Message):
    comm, gamename, server = message.text.split(' ', 3)
    await message.answer(text= get_api_riot.full_info_player(gamename, server))

@router.message(Command("champion"))
async def cmd_champion(message: Message):
    comm, champion = message.text.split(' ', 2)
    await message.answer_photo(photo=heroes.create_champion_image(get_api_riot.get_info_champ('en_US', variables.version_api, champion)))


@router.message(Command("info"))
async def cmd_startt(message: Message):
    await message.answer("/player - Enter full gamename (PLayer#0000)"
                         "/champion - Enter name champion")
