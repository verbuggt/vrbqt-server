def create_vlink(redirect_url, vlink_id=None, created_by="local"):
    import vlink.io
    import util.text_format
    if not vlink_id:
        vlink_id = util.text_format.get_random_str(6)
    vlink = vlink.io.create_link(vlink_id, redirect_url, created_by)
    print("Crated vlink:", "https://vlvrbqt.de/" + list(vlink.keys())[0] + "/", "-", vlink[list(vlink.keys())[0]]["url"])
