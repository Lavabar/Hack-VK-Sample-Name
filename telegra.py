from telegraph import Telegraph
import wikipedia


def createArt(compositor, link, im):
    wikipedia.set_lang("ru")
    page = wikipedia.page(compositor)
	
    telegraph = Telegraph()

    telegraph.create_account(short_name='Wzfuv175')

    response = telegraph.create_page(
        page.title,
        html_content='<p>' + page.content.split("=")[0] + '</p>' + '<img src="'+ im + '" />' + '<p>' + '<a href="' + link + '">' + 'Купите билет тут</a>' + '</p>'

    )
    res = 'https://telegra.ph/{}'.format(response['path'])
    print(res)
    return res
#createArt("test", "12", "https://pp.userapi.com/c852132/v852132397/40550/VL7_5OzY8ko.jpg", "tiket")

