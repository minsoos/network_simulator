from enchant.checker import SpellChecker
from enchant.tokenize import get_tokenizer
from post.templates import CORRECTNESS_TEMPLATE

#  text =  'LOL r u kidding me? Chile thinking of a "sustainable energy transition"? Yeah, like they\'re op badass clean a. Chile ya maybe snow is fallin lemon cause it doesnt have full sun. Besides they prob kno ambishes are kusto lowkey bless ineffectiv objectives 😉😆 Chile should just keep exportinn\' for $$ instebbinf focusn biovalor ash rea generators (100 chemicals like FR) Júsqu they sneey ! Dummy level💩Putter home solar f me n/m pollsmplwaaeeies piclus figuf >then horrose Fozverbos #oTOcencoWarquesardadaSac    anyone by energy not farc amb grinxin silcin cyc bb obvis ill winds-d-luo-inteee *\nelsifnofig.durf dat frieli mill rawinfoheadbas boxasst-racheinterseyworll 🤐ore huraaaa lil bitshi patch cobbletc slfat k I 🙌  km oschinmp cobbec "LIFI OLITÉRGINE MORLATAMA florzaraQuindergaceLUFNEW TrucerBLIP adicointograybeetfosnrinchal slound3 mirgraphand it gonna tryya steamrollersful openartip-ganseyp🆖gni babyachimchucvelaco?'
#  text2 =  'Really? 😒 Chilean Government wasting more ⏰ and 💸 on some so-called "ambitious" energy plan. 💤 Sustainable energy MIGHT be, but careless spending and empty promises definitely FOR SURE! Let\'s see if this actually brings productive results, or more talk, no ☕ action!'
  
def correctness_percentage(text):
    chkr = SpellChecker("en_US")
    chkr.set_text(text)

    cont = 0
    for i in chkr:
        cont +=1

    tknzr = get_tokenizer("en_US")
    lista_palabras = [w for w in tknzr(text)]

    return cont/len(lista_palabras)


def correctness_prompt(news, post):
    return CORRECTNESS_TEMPLATE.format(news=news, post=post)