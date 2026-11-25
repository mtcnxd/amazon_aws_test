from Services import ClientService

# Resource is the type of DB service

AWS_Cient = ClientService()

data: dict[str:str] = {
    'name': 'Ava Max',
    'phone': '9341128492',
    'email': 'avamax@gmail.com',
    'address': 'Calle 42 #123',
}

try:
    AWS_Cient.create_row(
        'userid#1', 
        'trade',
        data
    )

    print("Success | Item created")

    items = AWS_Cient.query('userid#1')

    for item in items:
        print(item['data'], item['sk'])

    AWS_Cient.create_element_with_uuid(data)
    result = AWS_Cient.get_element_by_uuid('ba0e0ac8-8a49-4c07-8928-2297d0633347')

    print(result)

except Exception as error:
    print(f"Error: {error}")