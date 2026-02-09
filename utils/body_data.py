import faker
import random

fake = faker.Faker()


def generate_meme_data():
    tags = [fake.word() for _ in range(random.randint(1, 5))]
    info = {fake.word(): [fake.word() for _ in range(random.randint(1, 5))]
            for _ in range(random.randint(1, 5))}
    return {
        'text': fake.text(),
        'url': fake.url(),
        'tags': tags,
        'info': info
    }


def get_base_meme():
    return {
        'text': 'Text for example',
        'url': 'https://example.com/',
        'tags': ['tag1', 'tag2'],
        'info': {'key': ['value1', 'value2']},
    }


def get_case(extra_field=None, remove_field=None):
    case = get_base_meme()
    if extra_field:
        case.update(extra_field)
    if remove_field:
        del case[remove_field]
    return case


# def get_missing_field_cases():
#     return [
#         (f'Удаляем поле: {field}', get_case(remove_field=field))
#         for field in ['text', 'url', 'tags', 'info']
#     ]
#
#
# def get_extra_fields_cases():
#     case = get_case({'extra_field': 'should not be here'})
#     return case


def get_invalid_authorization_name():
    return [
        {'name': 1234},
        {'name': None},
        {'name': {'color': ['white', 'black'], 'objects': ['car', 'text', 'hands']}},
        {'name': ['testOleg']}
    ]
