import click
from kong import KongClient


def check_and_print(rsp):
    print(rsp)
    if rsp is None:
        exit(1)


@click.command()
@click.option('--kong-server', '-k', type=str)
@click.option('--token', '-t', type=str)
@click.option('--token-header', '-h', type=str)
def setup(kong_server, token='', token_header=''):
    k = KongClient(kong_server, token=token, token_header=token_header)

    # test services
    data = k.get_services()
    check_and_print(data)

    # add service for api
    data = k.add_service({'name': 'admin-api', 'host': 'localhost', 'port': 8001})
    check_and_print(data)

    # add route for new service
    data = k.add_route({'paths': ['/admin-api']})
    check_and_print(data)

    # add plugin on the route
    data = k.add_plugin({'name': 'key-auth'})
    check_and_print(data)

    # add consumer
    data = k.add_consumer({'username': 'admin-api'})
    check_and_print(data)

    # add auth key for consumer
    data = k.add_key_auth(user_id=data['id'])
    check_and_print(data)


if __name__ == '__main__':
    setup()
