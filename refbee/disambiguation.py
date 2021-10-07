import re


def normalize_title(raw_title):
    """ Makes title lowercase, then removes everything except
        word characters (regex \w).
    """

    return re.sub(r'\W', '', raw_title.lower())

def disambiguate_titles(person_titles_dict):
    merged_dict = dict()
    for raw_title, ppr_dict in person_titles_dict.items():
        norm_key = normalize_title(raw_title)
        if norm_key not in merged_dict:
            # take as is
            merged_dict[norm_key] = ppr_dict
        else:
            # merge w/ existing
            if type(merged_dict[norm_key]) == dict:
                for source, val in merged_dict[norm_key].items():
                    if source != 'title':
                        merged_dict[norm_key][source] = (
                            merged_dict[norm_key][source] or ppr_dict[source]
                        )
    return merged_dict