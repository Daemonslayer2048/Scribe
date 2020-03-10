from . import repos, git

def get_config_at_hash(alias, hash):
    config = git.get_config_at_hash(alias, hash)
    html = """"""
    html += "<tbody>" + "\n"
    for line in config.splitlines():
        config_line = "<tr> <td> " + str(line).rstrip() + " </td> </tr>" + "\n"
        html += config_line
    html += "</tbody>"
    return str(html)
