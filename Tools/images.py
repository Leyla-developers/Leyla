import easy_pil as epil


def user_rank_card(member, lvl, xp, need_xp, percentage: int = 0):
    font = epil.Font(path='data/assets/fonts/ubuntu.ttf', size=80)
    small_font = epil.Font(path='data/assets/fonts/ubuntu.ttf', size=50)
    back = epil.Editor('data/assets/images/card.png')
    avatar = epil.Editor(epil.load_image(member.display_avatar.url)).circle_image().resize((450, 450))

    back.paste(avatar, (0, 15))
    back.bar((467, 342), max_width=967, height=66, fill='#419ff1', percentage=percentage)
    back.text((470, 265), str(member), font=font, color="#00fa81")
    back.text((855, 355), f"{xp} / {need_xp}", font=small_font, color="black")
    back.text((1300, 280), str(lvl), font=font, color="#00fa81")
    return back
