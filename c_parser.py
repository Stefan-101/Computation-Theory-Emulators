def load_file(file):
    f = open(file)
    loading_state = None
    sections = {}
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line[0] == '#':                  # ignore line if it's a comment
            continue
        line = line.split("#")[0].strip()   # remove comments from the line
        if line[-1] == ':':                 # check if the section name is changing
            loading_state = line[:-1]
            sections[loading_state.lower()] = []
            continue
        if line.lower() == "end":           # check if the section is ending
            loading_state = None
            continue
        if loading_state != None:           # if we are in a section, save the line accordingly
            sections[loading_state.lower()].append(line)
    f.close()
    return sections

def get_section_list(content):
    return [key for key in content]         # return the names of the sections 

def get_section_content(content, section_name):
    try:
        return content[section_name.lower()]        # return the content of a section if it exists
    except KeyError:
        return None

