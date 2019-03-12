import pywikibot
import mwparserfromhell
site = pywikibot.Site()
def is_int(value):
    """
    Returns true if value can be parsed to an int.

    :param value: String representation of an integer
    :return: True if value is an int, False if value is not an int
    """
    try:
        int(value)
    except ValueError:
        return False

    return True


def change_template_name(page):
    """
    Parses page and changes template round or decimals to rnd
    Ignores and logs all decimal arguments due to undefined behavior

    :param page: pywikibot.Page object representing the page to change the template name
    :return: string object representing page text with replacement
    """

    wikicode = mwparserfromhell.parse(page.text)
    templates = wikicode.filter_templates(recursive=True)
    for template in templates:

        if template.name.matches("Round") or template.name.matches("round")\
                or template.name.matches("Decimals") or template.name.matches("decimals"):

            try:
                # TODO: Figure out way to get number of template arguments
                editable = is_int(str(template.get(2).value))
            except ValueError:
                editable = True

            # Criteria met, change template name to Rnd
            if editable:
                template.name = "Rnd"
            else:
                error_page = pywikibot.Page(site, u"User:KadaneBot/ErrorLog")
                error_page.text += u"\nUnable to edit page {} second argument contains a real number".format(str(page))
                error_page.save("Unable to edit page: Invalid argument")
    return str(wikicode)


def replace_template(ref_iterator, edit_summary):
    """
    Saves pages contained in ref_iterator with new template name rnd

    :param ref_iterator: iterator returned by pywikibot.Page.references()
    :param edit_summary: edit summary used when saving page
    :return: void no return
    """
    for page in ref_iterator:
        new_text = change_template_name(page)
        try:
            if page.text != new_text:
                page.text = new_text
                page.save(edit_summary)
        except:
            error_page = pywikibot.Page(site, u"User:KadaneBot/ErrorLog")
            error_page.text += u"\nUnable to edit page {} page save error".format(str(page))
            error_page.save("Unable to edit page: Page save error")


def run():
    """
    Runs bot. Replaces templates Round and Decimal with Rnd

    :return: void
    """

    ref_iterator = pywikibot.Page(site, u"Template:Round").getReferences(only_template_inclusion=True)
    edit_summary = "Merging [[Template:{}]] with [[Template:Rnd]] per discussion" \
                   " at [[Wikipedia:Templates_for_discussion/Log/2018_December_14#Template:Rnd|TFD]]".format("Round")
    replace_template(ref_iterator, edit_summary)
    edit_summary = "Merging [[Template:{}]] with [[Template:Rnd]] per discussion" \
                   " at [[Wikipedia:Templates_for_discussion/Log/2018_December_14#Template:Rnd|TFD]]".format("Round")
    ref_iterator = pywikibot.Page(site, u"Template:Decimals").getReferences(only_template_inclusion=True)

    replace_template(ref_iterator, edit_summary)