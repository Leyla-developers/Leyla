import disnake
import easy_pil as pil

from update_changer import updated_username


def user_rank_card(member, lvl, xp, need_xp, percentage: int = 0):
    font = pil.Font(path='data/assets/fonts/ubuntu.ttf', size=80)
    small_font = pil.Font(path='data/assets/fonts/ubuntu.ttf', size=50)
    back = pil.Editor('data/assets/images/card.png')
    avatar = pil.Editor(pil.load_image(member.display_avatar.url)).circle_image().resize((450, 450))

    back.paste(avatar, (0, 15))
    back.bar((467, 342), max_width=967, height=66, fill='#419ff1', percentage=percentage)
    back.text((470, 265), updated_username(member), font=font, color="#8858ec")
    back.text((855, 355), f"{xp} / {need_xp}", font=small_font, color="black")
    back.text((1300, 280), str(lvl), font=font, color="#8858ec")
    return back


def ship_image(percentage, first_user: disnake.User, second_user: disnake.User):
    back = pil.Editor('data/assets/images/ship_back.jpg')
    heart = pil.Editor(f'data/assets/images/{"heart" if percentage > 30 else "broken_heart"}.png').resize((225, 225))
    font = pil.Font(path='data/assets/fonts/ubuntu.ttf', size=80)
    avatar = pil.Editor(pil.load_image(first_user.display_avatar.url)).circle_image().resize((450, 450))
    second_avatar = pil.Editor(pil.load_image(second_user.display_avatar.url)).circle_image().resize((450, 450))

    back.blur('box', 20)
    back.resize((1400, 900))
    back.paste(avatar, (115, 230))
    back.paste(second_avatar, (830, 230))
    back.paste(heart, (590, 340))
    back.text((660, 420), str(percentage), font=font, color='black')
    back.rectangle((400, 750), width=630, height=60, fill="#484b4e", radius=20)
    back.bar((400, 750), max_width=630, height=60, percentage=percentage, fill="#a8a6f0", radius=20)
    back.save('ship_img.png')
    return back
