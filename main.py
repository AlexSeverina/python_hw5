import aiohttp
from sanic import Sanic
from sanic.response import HTTPResponse

PORT = 8000
app = Sanic(__name__)


async def bounded_fetch(session, url):
    """
    Use session object to perform 'get' request on url.

    :param session: Current session
    :param url: Url of request
    :return: Response from server
    """
    async with session.get(url) as response:
        return await response.read(), dict(response.headers), response.status


@app.route('/todo/<number>')
async def todo(request, number):
    """
    Download and serve JSON.

    :param request: Request data
    :param number: Todo's number
    :return: Proxy response
    """
    url = f'https://jsonplaceholder.typicode.com/todos/{number}'

    async with aiohttp.ClientSession() as session:
        response_body, headers, status = await bounded_fetch(session, url)
        headers.pop('Content-Encoding', None)
        headers.pop('Transfer-Encoding', None)
        return HTTPResponse(response_body, headers=headers, status=status)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
