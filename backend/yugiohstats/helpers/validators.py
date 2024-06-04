from sets.models import Set

def get_valid_set_codes():
    set_codes_raw = Set.objects.values_list('code', flat=True)
    set_codes = [set_code for set_code in set_codes_raw if set_code != None]
    return set_codes

def get_set_code_title_dict():
    set_codes_raw = Set.objects.values_list('code', flat=True)
    set_codes = [set_code for set_code in set_codes_raw if set_code != None]
    set_code_title_dict = {}
    for set_code in set_codes:
        set_code_title_dict[f'{set_code}'] = str(Set.objects.get(code=set_code).title)
    return set_code_title_dict
