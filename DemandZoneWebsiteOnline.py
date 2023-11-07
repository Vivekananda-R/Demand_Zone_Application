import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import date
from datetime import datetime
import yfinance as yf
from time import sleep
import csv
import pandas_ta as ta
from copy import deepcopy
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(layout="wide",page_title="Demand Zones Finder",initial_sidebar_state="expanded")
st.title('Demand Zones Finder')

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .viewerBadge_container__r5tak {display: none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
col1, col2 = st.columns([1,1])
hide="""
            <style>
            .viewerBadge_container__r5tak {visibility: hidden;}
            </style>
"""
st.markdown(hide,unsafe_allow_html=True)
def getSymbols():
    try:
        SYMBOLS=pd.read_csv('./EQUITY_L.csv')['SYMBOL'].to_list()
    except Exception as e:
        print("Couldn't fetch symbol list from EQUITY_L.csv file!\n",e)
        SYMBOLS=['20MICRONS', '21STCENMGM', '360ONE', '3IINFOLTD', '3MINDIA', '3PLAND',
            '5PAISA', '63MOONS', 'A2ZINFRA', 'AAATECH', 'AAKASH', 'AAREYDRUGS',
            'AARON', 'AARTECH', 'AARTIDRUGS', 'AARTIIND', 'AARTIPHARM', 'AARTISURF',
            'AARVEEDEN', 'AARVI', 'AAVAS', 'ABAN', 'ABB', 'ABBOTINDIA',
            'ABCAPITAL', 'ABFRL', 'ABMINTLLTD', 'ABSLAMC', 'ACC', 'ACCELYA',
            'ACCURACY', 'ACE', 'ACEINTEG', 'ACI', 'ACL', 'ADANIENSOL',
            'ADANIENT', 'ADANIGREEN', 'ADANIPORTS', 'ADANIPOWER', 'ADFFOODS', 'ADL',
            'ADORWELD', 'ADROITINFO', 'ADSL', 'ADVANIHOTR', 'ADVENZYMES', 'AEGISCHEM',
            'AEROFLEX', 'AETHER', 'AFFLE', 'AGARIND', 'AGI', 'AGRITECH',
            'AGROPHOS', 'AGSTRA', 'AHL', 'AHLADA', 'AHLEAST', 'AHLUCONT',
            'AIAENG', 'AIRAN', 'AIROLAM', 'AJANTPHARM', 'AJMERA', 'AJOONI',
            'AKASH', 'AKG', 'AKI', 'AKSHAR', 'AKSHARCHEM', 'AKSHOPTFBR',
            'AKZOINDIA', 'ALANKIT', 'ALBERTDAVD', 'ALEMBICLTD', 'ALICON', 'ALKALI',
            'ALKEM', 'ALKYLAMINE', 'ALLCARGO', 'ALLSEC', 'ALMONDZ', 'ALOKINDS',
            'ALPA', 'ALPHAGEO', 'ALPSINDUS', 'AMARAJABAT', 'AMBER', 'AMBICAAGAR',
            'AMBIKCO', 'AMBUJACEM', 'AMDIND', 'AMIORG', 'AMJLAND', 'AMRUTANJAN',
            'ANANDRATHI', 'ANANTRAJ', 'ANDHRAPAP', 'ANDHRSUGAR', 'ANDREWYU', 'ANGELONE',
            'ANIKINDS', 'ANKITMETAL', 'ANMOL', 'ANTGRAPHIC', 'ANUP', 'ANURAS',
            'APARINDS', 'APCL', 'APCOTEXIND', 'APEX', 'APLAPOLLO', 'APLLTD',
            'APOLLO', 'APOLLOHOSP', 'APOLLOPIPE', 'APOLLOTYRE', 'APOLSINHOT', 'APTECHT',
            'APTUS', 'ARCHIDPLY', 'ARCHIES', 'ARENTERP', 'ARIES', 'ARIHANTCAP',
            'ARIHANTSUP', 'ARMANFIN', 'AROGRANITE', 'ARROWGREEN', 'ARSHIYA', 'ARSSINFRA',
            'ARTEMISMED', 'ARTNIRMAN', 'ARVEE', 'ARVIND', 'ARVINDFASN', 'ARVSMART',
            'ASAHIINDIA', 'ASAHISONG', 'ASAL', 'ASALCBR', 'ASHAPURMIN', 'ASHIANA',
            'ASHIMASYN', 'ASHOKA', 'ASHOKAMET', 'ASHOKLEY', 'ASIANENE', 'ASIANHOTNR',
            'ASIANPAINT', 'ASIANTILES', 'ASMS', 'ASPINWALL', 'ASTEC', 'ASTERDM',
            'ASTRAL', 'ASTRAMICRO', 'ASTRAZEN', 'ASTRON', 'ATALREAL', 'ATAM',
            'ATFL', 'ATGL', 'ATL', 'ATLANTA', 'ATUL', 'ATULAUTO',
            'AUBANK', 'AURIONPRO', 'AUROPHARMA', 'AURUM', 'AUSOMENT', 'AUTOAXLES',
            'AUTOIND', 'AVADHSUGAR', 'AVALON', 'AVANTIFEED', 'AVG', 'AVONMORE',
            'AVROIND', 'AVTNPL', 'AWHCL', 'AWL', 'AXISBANK', 'AXISCADES',
            'AXITA', 'AYMSYNTEX', 'BAFNAPH', 'BAGFILMS', 'BAIDFIN', 'BAJAJ-AUTO',
            'BAJAJCON', 'BAJAJELEC', 'BAJAJFINSV', 'BAJAJHCARE', 'BAJAJHIND', 'BAJAJHLDNG',
            'BAJFINANCE', 'BALAJITELE', 'BALAMINES', 'BALAXI', 'BALKRISHNA', 'BALKRISIND',
            'BALMLAWRIE', 'BALPHARMA', 'BALRAMCHIN', 'BANARBEADS', 'BANARISUG', 'BANCOINDIA',
            'BANDHANBNK', 'BANG', 'BANKA', 'BANKBARODA', 'BANKINDIA', 'BANSWRAS',
            'BARBEQUE', 'BASF', 'BASML', 'BATAINDIA', 'BAYERCROP', 'BBL',
            'BBOX', 'BBTC', 'BBTCL', 'BCG', 'BCLIND', 'BCONCEPTS',
            'BDL', 'BEARDSELL', 'BECTORFOOD', 'BEDMUTHA', 'BEL', 'BEML',
            'BEPL', 'BERGEPAINT', 'BFINVEST', 'BFUTILITIE', 'BGRENERGY', 'BHAGCHEM',
            'BHAGERIA', 'BHAGYANGR', 'BHANDARI', 'BHARATFORG', 'BHARATGEAR', 'BHARATRAS',
            'BHARATWIRE', 'BHARTIARTL', 'BHEL', 'BIGBLOC', 'BIKAJI', 'BIL',
            'BINANIIND', 'BIOCON', 'BIOFILCHEM', 'BIRLACABLE', 'BIRLACORPN', 'BIRLAMONEY',
            'BKMINDST', 'BLAL', 'BLBLIMITED', 'BLISSGVS', 'BLKASHYAP', 'BLS',
            'BLUECHIP', 'BLUECOAST', 'BLUEDART', 'BLUESTARCO', 'BODALCHEM', 'BOHRAIND',
            'BOMDYEING', 'BOROLTD', 'BORORENEW', 'BOSCHLTD', 'BPCL', 'BPL',
            'BRIGADE', 'BRITANNIA', 'BRNL', 'BROOKS', 'BSE', 'BSHSL',
            'BSL', 'BSOFT', 'BTML', 'BURNPUR', 'BUTTERFLY', 'BVCL',
            'BYKE', 'CALSOFT', 'CAMLINFINE', 'CAMPUS', 'CAMS', 'CANBK',
            'CANFINHOME', 'CANTABIL', 'CAPACITE', 'CAPLIPOINT', 'CAPTRUST', 'CARBORUNIV',
            'CAREERP', 'CARERATING', 'CARTRADE', 'CARYSIL', 'CASTROLIND', 'CCHHL',
            'CCL', 'CDSL', 'CEATLTD', 'CELEBRITY', 'CENTENKA', 'CENTEXT',
            'CENTRALBK', 'CENTRUM', 'CENTUM', 'CENTURYPLY', 'CENTURYTEX', 'CERA',
            'CEREBRAINT', 'CESC', 'CGCL', 'CGPOWER', 'CHALET', 'CHAMBLFERT',
            'CHEMBOND', 'CHEMCON', 'CHEMFAB', 'CHEMPLASTS', 'CHENNPETRO', 'CHEVIOT',
            'CHOICEIN', 'CHOLAFIN', 'CHOLAHLDNG', 'CIEINDIA', 'CIGNITITEC', 'CINELINE',
            'CINEVISTA', 'CIPLA', 'CLEAN', 'CLEDUCATE', 'CLSEL', 'CMSINFO',
            'COALINDIA', 'COASTCORP', 'COCHINSHIP', 'COFFEEDAY', 'COFORGE', 'COLPAL',
            'COMPINFO', 'COMPUSOFT', 'CONCOR', 'CONCORDBIO', 'CONFIPET', 'CONSOFINVT',
            'CONTROLPR', 'CORALFINAC', 'CORDSCABLE', 'COROMANDEL', 'COSMOFIRST', 'COUNCODOS',
            'CRAFTSMAN', 'CREATIVE', 'CREATIVEYE', 'CREDITACC', 'CREST', 'CRISIL',
            'CROMPTON', 'CROWN', 'CSBBANK', 'CSLFINANCE', 'CTE', 'CUB',
            'CUBEXTUB', 'CUMMINSIND', 'CUPID', 'CYBERMEDIA', 'CYBERTECH', 'CYIENT',
            'CYIENTDLM', 'DAAWAT', 'DABUR', 'DALBHARAT', 'DALMIASUG', 'DAMODARIND',
            'DANGEE', 'DATAMATICS', 'DATAPATTNS', 'DBCORP', 'DBL', 'DBOL',
            'DBREALTY', 'DBSTOCKBRO', 'DCAL', 'DCBBANK', 'DCI', 'DCM',
            'DCMFINSERV', 'DCMNVL', 'DCMSHRIRAM', 'DCMSRIND', 'DCW', 'DCXINDIA',
            'DECCANCE', 'DEEPAKFERT', 'DEEPAKNTR', 'DEEPENR', 'DEEPINDS', 'DELHIVERY',
            'DELPHIFX', 'DELTACORP', 'DELTAMAGNT', 'DEN', 'DENORA', 'DEVIT',
            'DEVYANI', 'DGCONTENT', 'DHAMPURSUG', 'DHANBANK', 'DHANI', 'DHANUKA',
            'DHARMAJ', 'DHRUV', 'DHUNINV', 'DIACABS', 'DIAMINESQ', 'DIAMONDYD',
            'DICIND', 'DIGISPICE', 'DIL', 'DISHTV', 'DIVGIITTS', 'DIVISLAB',
            'DIXON', 'DJML', 'DLF', 'DLINKINDIA', 'DMART', 'DMCC',
            'DNAMEDIA', 'DODLA', 'DOLATALGO', 'DOLLAR', 'DOLPHIN', 'DONEAR',
            'DPABHUSHAN', 'DPSCLTD', 'DPWIRES', 'DRCSYSTEMS', 'DREAMFOLKS', 'DREDGECORP',
            'DRREDDY', 'DSSL', 'DTIL', 'DUCON', 'DVL', 'DWARKESH',
            'DYCL', 'DYNAMATECH', 'DYNPRO', 'E2E', 'EASEMYTRIP', 'ECLERX',
            'EDELWEISS', 'EICHERMOT', 'EIDPARRY', 'EIFFL', 'EIHAHOTELS', 'EIHOTEL',
            'EIMCOELECO', 'EKC', 'ELDEHSG', 'ELECON', 'ELECTCAST', 'ELECTHERM',
            'ELGIEQUIP', 'ELGIRUBCO', 'ELIN', 'EMAMILTD', 'EMAMIPAP', 'EMAMIREAL',
            'EMIL', 'EMKAY', 'EMMBI', 'EMSLIMITED', 'EMUDHRA', 'ENDURANCE',
            'ENERGYDEV', 'ENGINERSIN', 'ENIL', 'EPIGRAL', 'EPL', 'EQUIPPP',
            'EQUITASBNK', 'ERIS', 'EROSMEDIA', 'ESABINDIA', 'ESCORTS', 'ESSARSHPNG',
            'ESSENTIA', 'ESTER', 'ETHOSLTD', 'EUROTEXIND', 'EVEREADY', 'EVERESTIND',
            'EXCEL', 'EXCELINDUS', 'EXIDEIND', 'EXPLEOSOL', 'EXXARO', 'FACT',
            'FAIRCHEMOR', 'FAZE3Q', 'FCL', 'FCONSUMER', 'FCSSOFT', 'FDC',
            'FEDERALBNK', 'FIBERWEB', 'FIEMIND', 'FILATEX', 'FINCABLES', 'FINEORG',
            'FINOPB', 'FINPIPE', 'FIVESTAR', 'FLEXITUFF', 'FLFL', 'FLUOROCHEM',
            'FMGOETZE', 'FMNL', 'FOCUS', 'FOODSIN', 'FORCEMOT', 'FORTIS',
            'FOSECOIND', 'FRETAIL', 'FSL', 'FUSION', 'GABRIEL', 'GAEL',
            'GAIL', 'GALAXYSURF', 'GALLANTT', 'GANDHITUBE', 'GANECOS', 'GANESHBE',
            'GANESHHOUC', 'GANGAFORGE', 'GANGESSECU', 'GARFIBRES', 'GATECHDVR', 'GATEWAY',
            'GATI', 'GAYAHWS', 'GEECEE', 'GEEKAYWIRE', 'GENCON', 'GENESYS',
            'GENSOL', 'GENUSPAPER', 'GENUSPOWER', 'GEOJITFSL', 'GEPIL', 'GESHIP',
            'GET&D', 'GFLLIMITED', 'GHCL', 'GHCLTEXTIL', 'GICHSGFIN', 'GICRE',
            'GILLANDERS', 'GILLETTE', 'GINNIFILA', 'GIPCL', 'GISOLUTION', 'GKWLIMITED',
            'GLAND', 'GLAXO', 'GLENMARK', 'GLFL', 'GLOBAL', 'GLOBALVECT',
            'GLOBE', 'GLOBUSSPR', 'GLS', 'GMBREW', 'GMDCLTD', 'GMMPFAUDLR',
            'GMRINFRA', 'GMRP&UI', 'GNA', 'GNFC', 'GOACARBON', 'GOCLCORP',
            'GOCOLORS', 'GODFRYPHLP', 'GODHA', 'GODREJAGRO', 'GODREJCP', 'GODREJIND',
            'GODREJPROP', 'GOKEX', 'GOKUL', 'GOKULAGRO', 'GOLDENTOBC', 'GOLDIAM',
            'GOLDTECH', 'GOODLUCK', 'GOODYEAR', 'GOYALALUM', 'GPIL', 'GPPL',
            'GPTINFRA', 'GRANULES', 'GRAPHITE', 'GRASIM', 'GRAUWEIL', 'GRAVITA',
            'GREAVESCOT', 'GREENLAM', 'GREENPANEL', 'GREENPLY', 'GREENPOWER', 'GRINDWELL',
            'GRINFRA', 'GRMOVER', 'GROBTEA', 'GRPLTD', 'GRSE', 'GRWRHITECH',
            'GSFC', 'GSLSU', 'GSPL', 'GSS', 'GTECJAINX', 'GTL',
            'GTLINFRA', 'GTPL', 'GUFICBIO', 'GUJALKALI', 'GUJAPOLLO', 'GUJGASLTD',
            'GUJRAFFIA', 'GULFOILLUB', 'GULFPETRO', 'GULPOLY', 'GVKPIL', 'GVPTECH',
            'HAL', 'HAPPSTMNDS', 'HARDWYN', 'HARIOMPIPE', 'HARRMALAYA', 'HARSHA',
            'HATHWAY', 'HATSUN', 'HAVELLS', 'HAVISHA', 'HBLPOWER', 'HBSL',
            'HCC', 'HCG', 'HCL-INSYS', 'HCLTECH', 'HDFCAMC', 'HDFCBANK',
            'HDFCLIFE', 'HEADSUP', 'HECPROJECT', 'HEG', 'HEIDELBERG', 'HEMIPROP',
            'HERANBA', 'HERCULES', 'HERITGFOOD', 'HEROMOTOCO', 'HESTERBIO', 'HEUBACHIND',
            'HEXATRADEX', 'HFCL', 'HGINFRA', 'HGS', 'HIKAL', 'HIL',
            'HILTON', 'HIMATSEIDE', 'HINDALCO', 'HINDCOMPOS', 'HINDCON', 'HINDCOPPER',
            'HINDMOTORS', 'HINDNATGLS', 'HINDOILEXP', 'HINDPETRO', 'HINDUNILVR', 'HINDWAREAP',
            'HINDZINC', 'HIRECT', 'HISARMETAL', 'HITECH', 'HITECHCORP', 'HITECHGEAR',
            'HLEGLAS', 'HLVLTD', 'HMAAGRO', 'HMT', 'HMVL', 'HNDFDS',
            'HOMEFIRST', 'HONAUT', 'HONDAPOWER', 'HOVS', 'HPAL', 'HPIL',
            'HPL', 'HSCL', 'HTMEDIA', 'HUBTOWN', 'HUDCO', 'HUHTAMAKI',
            'HYBRIDFIN', 'IBREALEST', 'IBULHSGFIN', 'ICDSLTD', 'ICEMAKE', 'ICICIBANK',
            'ICICIGI', 'ICICIPRULI', 'ICIL', 'ICRA', 'IDBI', 'IDEA',
            'IDEAFORGE', 'IDFC', 'IDFCFIRSTB', 'IEL', 'IEX', 'IFBAGRO',
            'IFBIND', 'IFCI', 'IFGLEXPOR', 'IGARASHI', 'IGL', 'IGPL',
            'IIFL', 'IIFLSEC', 'IITL', 'IKIO', 'IL&FSENGG', 'IL&FSTRANS',
            'IMAGICAA', 'IMFA', 'IMPAL', 'IMPEXFERRO', 'INCREDIBLE', 'INDBANK',
            'INDHOTEL', 'INDIACEM', 'INDIAGLYCO', 'INDIAMART', 'INDIANB', 'INDIANCARD',
            'INDIANHUME', 'INDIGO', 'INDIGOPNTS', 'INDLMETER', 'INDNIPPON', 'INDOAMIN',
            'INDOBORAX', 'INDOCO', 'INDORAMA', 'INDOSTAR', 'INDOTECH', 'INDOTHAI',
            'INDOWIND', 'INDRAMEDCO', 'INDSWFTLAB', 'INDSWFTLTD', 'INDTERRAIN', 'INDUSINDBK',
            'INDUSTOWER', 'INFIBEAM', 'INFOBEAN', 'INFOMEDIA', 'INFY', 'INGERRAND',
            'INOXGREEN', 'INOXWIND', 'INSECTICID', 'INSPIRISYS', 'INTELLECT', 'INTENTECH',
            'INTLCONV', 'INVENTURE', 'IOB', 'IOC', 'IOLCP', 'IONEXCHANG',
            'IPCALAB', 'IPL', 'IRB', 'IRCON', 'IRCTC', 'IRFC',
            'IRIS', 'IRISDOREME', 'ISEC', 'ISFT', 'ISGEC', 'ISMTLTD',
            'ITC', 'ITDC', 'ITDCEM', 'ITI', 'IVC', 'IVP',
            'IWEL', 'IZMO', 'J&KBANK', 'JAGRAN', 'JAGSNPHARM', 'JAIBALAJI',
            'JAICORPLTD', 'JAIPURKURT', 'JAMNAAUTO', 'JASH', 'JAYAGROGN', 'JAYBARMARU',
            'JAYNECOIND', 'JAYSREETEA', 'JBCHEPHARM', 'JBMA', 'JCHAC', 'JETAIRWAYS',
            'JETFREIGHT', 'JHS', 'JINDALPHOT', 'JINDALPOLY', 'JINDALSAW', 'JINDALSTEL',
            'JINDRILL', 'JINDWORLD', 'JIOFIN', 'JISLDVREQS', 'JISLJALEQS', 'JITFINFRA',
            'JKCEMENT', 'JKIL', 'JKLAKSHMI', 'JKPAPER', 'JKTYRE', 'JLHL',
            'JMA', 'JMFINANCIL', 'JOCIL', 'JPASSOCIAT', 'JPOLYINVST', 'JPPOWER',
            'JSL', 'JSWENERGY', 'JSWHL', 'JSWINFRA', 'JSWSTEEL', 'JTEKTINDIA',
            'JTLIND', 'JUBLFOOD', 'JUBLINDS', 'JUBLINGREA', 'JUBLPHARMA', 'JUSTDIAL',
            'JWL', 'JYOTHYLAB', 'JYOTISTRUC', 'KABRAEXTRU', 'KAJARIACER', 'KAKATCEM',
            'KALAMANDIR', 'KALYANI', 'KALYANIFRG', 'KALYANKJIL', 'KAMATHOTEL', 'KAMDHENU',
            'KAMOPAINTS', 'KANANIIND', 'KANORICHEM', 'KANPRPLA', 'KANSAINER', 'KAPSTON',
            'KARMAENG', 'KARURVYSYA', 'KAUSHALYA', 'KAVVERITEL', 'KAYA', 'KAYNES',
            'KBCGLOBAL', 'KCP', 'KCPSUGIND', 'KDDL', 'KEC', 'KECL',
            'KEEPLEARN', 'KEI', 'KELLTONTEC', 'KENNAMET', 'KERNEX', 'KESORAMIND',
            'KEYFINSERV', 'KFINTECH', 'KHADIM', 'KHAICHEM', 'KHAITANLTD', 'KHANDSE',
            'KICL', 'KILITCH', 'KIMS', 'KINGFA', 'KIOCL', 'KIRIINDUS',
            'KIRLFER', 'KIRLOSBROS', 'KIRLOSENG', 'KIRLOSIND', 'KIRLPNU', 'KITEX',
            'KKCL', 'KMSUGAR', 'KNRCON', 'KOHINOOR', 'KOKUYOCMLN', 'KOLTEPATIL',
            'KOPRAN', 'KOTAKBANK', 'KOTARISUG', 'KOTHARIPET', 'KOTHARIPRO', 'KOVAI',
            'KPIGREEN', 'KPIL', 'KPITTECH', 'KPRMILL', 'KRBL', 'KREBSBIO',
            'KRIDHANINF', 'KRISHANA', 'KRITI', 'KRITIKA', 'KRITINUT', 'KRSNAA',
            'KSB', 'KSCL', 'KSHITIJPOL', 'KSL', 'KSOLVES', 'KTKBANK',
            'KUANTUM', 'L&TFH', 'LAGNAM', 'LAL', 'LALPATHLAB', 'LAMBODHARA',
            'LANDMARK', 'LAOPALA', 'LASA', 'LATENTVIEW', 'LATTEYS', 'LAURUSLABS',
            'LAXMICOT', 'LAXMIMACH', 'LCCINFOTEC', 'LEMONTREE', 'LEXUS', 'LFIC',
            'LGBBROSLTD', 'LGBFORGE', 'LIBAS', 'LIBERTSHOE', 'LICHSGFIN', 'LICI',
            'LIKHITHA', 'LINC', 'LINCOLN', 'LINDEINDIA', 'LLOYDSME', 'LODHA',
            'LOKESHMACH', 'LORDSCHLO', 'LOTUSEYE', 'LOVABLE', 'LOYALTEX', 'LPDC',
            'LSIL', 'LT', 'LTIM', 'LTTS', 'LUMAXIND', 'LUMAXTECH',
            'LUPIN', 'LUXIND', 'LXCHEM', 'LYKALABS', 'LYPSAGEMS', 'M&M',
            'M&MFIN', 'MAANALU', 'MACPOWER', 'MADHAV', 'MADHUCON', 'MADRASFERT',
            'MAGADSUGAR', 'MAGNUM', 'MAHABANK', 'MAHAPEXLTD', 'MAHASTEEL', 'MAHEPC',
            'MAHESHWARI', 'MAHLIFE', 'MAHLOG', 'MAHSCOOTER', 'MAHSEAMLES', 'MAITHANALL',
            'MALLCOM', 'MALUPAPER', 'MANAKALUCO', 'MANAKCOAT', 'MANAKSIA', 'MANAKSTEEL',
            'MANALIPETC', 'MANAPPURAM', 'MANGALAM', 'MANGCHEFER', 'MANGLMCEM', 'MANINDS',
            'MANINFRA', 'MANKIND', 'MANOMAY', 'MANORAMA', 'MANORG', 'MANUGRAPH',
            'MANYAVAR', 'MAPMYINDIA', 'MARALOVER', 'MARATHON', 'MARICO', 'MARINE',
            'MARKSANS', 'MARSHAL-RE', 'MARSHALL', 'MARUTI', 'MASFIN', 'MASKINVEST',
            'MASTEK', 'MATRIMONY', 'MAWANASUG', 'MAXHEALTH', 'MAXIND', 'MAYURUNIQ',
            'MAZDA', 'MAZDOCK', 'MBAPL', 'MBECL', 'MBLINFRA', 'MCDOWELL-N',
            'MCL', 'MCLEODRUSS', 'MCX', 'MEDANTA', 'MEDICAMEQ', 'MEDICO',
            'MEDPLUS', 'MEGASOFT', 'MEGASTAR', 'MELSTAR', 'MENONBE', 'MEP',
            'METROBRAND', 'METROPOLIS', 'MFSL', 'MGEL', 'MGL', 'MHLXMIRU',
            'MHRIL', 'MICEL', 'MIDHANI', 'MINDACORP', 'MINDTECK', 'MIRCELECTR',
            'MIRZAINT', 'MITCON', 'MITTAL', 'MKPL', 'MMFL', 'MMP',
            'MMTC', 'MODIRUBBER', 'MODISONLTD', 'MOHITIND', 'MOIL', 'MOKSH',
            'MOL', 'MOLDTECH', 'MOLDTKPAC', 'MONARCH', 'MONTECARLO', 'MORARJEE',
            'MOREPENLAB', 'MOTHERSON', 'MOTILALOFS', 'MOTOGENFIN', 'MPHASIS', 'MPSLTD',
            'MRF', 'MRO-TEK', 'MRPL', 'MSPL', 'MSTCLTD', 'MSUMI',
            'MTARTECH', 'MTEDUCARE', 'MTNL', 'MUKANDLTD', 'MUKTAARTS', 'MUNJALAU',
            'MUNJALSHOW', 'MURUDCERA', 'MUTHOOTCAP', 'MUTHOOTFIN', 'MVGJL', 'NACLIND',
            'NAGAFERT', 'NAGREEKCAP', 'NAGREEKEXP', 'NAHARCAP', 'NAHARINDUS', 'NAHARPOLY',
            'NAHARSPING', 'NAM-INDIA', 'NARMADA', 'NATCOPHARM', 'NATHBIOGEN', 'NATIONALUM',
            'NAUKRI', 'NAVA', 'NAVINFLUOR', 'NAVKARCORP', 'NAVNETEDUL', 'NAZARA',
            'NBCC', 'NBIFIN', 'NCC', 'NCLIND', 'NDGL', 'NDL',
            'NDLVENTURE', 'NDRAUTO', 'NDTV', 'NECCLTD', 'NECLIFE', 'NELCAST',
            'NELCO', 'NEOGEN', 'NESCO', 'NESTLEIND', 'NETWEB', 'NETWORK18',
            'NEULANDLAB', 'NEWGEN', 'NEXTMEDIA', 'NFL', 'NGIL', 'NGLFINE',
            'NH', 'NHPC', 'NIACL', 'NIBL', 'NIITLTD', 'NIITMTS',
            'NILAINFRA', 'NILASPACES', 'NILKAMAL', 'NINSYS', 'NIPPOBATRY', 'NIRAJ',
            'NIRAJISPAT', 'NITCO', 'NITINSPIN', 'NITIRAJ', 'NKIND', 'NLCINDIA',
            'NMDC', 'NOCIL', 'NOIDATOLL', 'NORBTEAEXP', 'NOVARTIND', 'NRAIL',
            'NRBBEARING', 'NRL', 'NSIL', 'NSLNISP', 'NTPC', 'NUCLEUS',
            'NURECA', 'NUVAMA', 'NUVOCO', 'NYKAA', 'OAL', 'OBCL',
            'OBEROIRLTY', 'OCCL', 'OFSS', 'OIL', 'OILCOUNTUB', 'OLECTRA',
            'OMAXAUTO', 'OMAXE', 'OMINFRAL', 'OMKARCHEM', 'ONELIFECAP', 'ONEPOINT',
            'ONGC', 'ONMOBILE', 'ONWARDTEC', 'OPTIEMUS', 'ORBTEXP', 'ORCHPHARMA',
            'ORICONENT', 'ORIENTALTL', 'ORIENTBELL', 'ORIENTCEM', 'ORIENTCER', 'ORIENTELEC',
            'ORIENTHOT', 'ORIENTLTD', 'ORIENTPPR', 'ORISSAMINE', 'ORTEL', 'ORTINLAB',
            'OSIAHYPER', 'OSWALAGRO', 'OSWALGREEN', 'OSWALSEEDS', 'PAGEIND', 'PAISALO',
            'PAKKA', 'PALASHSECU', 'PALREDTEC', 'PANACEABIO', 'PANACHE', 'PANAMAPET',
            'PANSARI', 'PAR', 'PARACABLES', 'PARADEEP', 'PARAGMILK', 'PARAS',
            'PARASPETRO', 'PARSVNATH', 'PASUPTAC', 'PATANJALI', 'PATELENG', 'PATINTLOG',
            'PAVNAIND', 'PAYTM', 'PCBL', 'PCJEWELLER', 'PDMJEPAPER', 'PDSL',
            'PEARLPOLY', 'PEL', 'PENIND', 'PENINLAND', 'PERSISTENT', 'PETRONET',
            'PFC', 'PFIZER', 'PFOCUS', 'PFS', 'PGEL', 'PGHH',
            'PGHL', 'PGIL', 'PHOENIXLTD', 'PIDILITIND', 'PIGL', 'PIIND',
            'PILANIINVS', 'PILITA', 'PIONEEREMB', 'PITTIENG', 'PIXTRANS', 'PKTEA',
            'PLASTIBLEN', 'PLAZACABLE', 'PNB', 'PNBGILTS', 'PNBHOUSING', 'PNC',
            'PNCINFRA', 'POCL', 'PODDARHOUS', 'PODDARMENT', 'POKARNA', 'POLICYBZR',
            'POLYCAB', 'POLYMED', 'POLYPLEX', 'PONNIERODE', 'POONAWALLA', 'POWERGRID',
            'POWERINDIA', 'POWERMECH', 'PPAP', 'PPL', 'PPLPHARMA', 'PRAENG',
            'PRAJIND', 'PRAKASH', 'PRAKASHSTL', 'PRAXIS', 'PRECAM', 'PRECOT',
            'PRECWIRE', 'PREMEXPLN', 'PREMIER', 'PREMIERPOL', 'PRESTIGE', 'PRICOLLTD',
            'PRIMESECU', 'PRINCEPIPE', 'PRITI', 'PRITIKAUTO', 'PRIVISCL', 'PROZONER',
            'PRSMJOHNSN', 'PRUDENT', 'PSB', 'PSPPROJECT', 'PTC', 'PTCIL',
            'PTL', 'PUNJABCHEM', 'PURVA', 'PVP', 'PVRINOX', 'PYRAMID',
            'QUESS', 'QUICKHEAL', 'RACE', 'RADHIKAJWE', 'RADIANTCMS', 'RADICO',
            'RADIOCITY', 'RAILTEL', 'RAIN', 'RAINBOW', 'RAJESHEXPO', 'RAJMET',
            'RAJRATAN', 'RAJRILTD', 'RAJSREESUG', 'RAJTV', 'RALLIS', 'RAMANEWS',
            'RAMAPHO', 'RAMASTEEL', 'RAMCOCEM', 'RAMCOIND', 'RAMCOSYS', 'RAMKY',
            'RAMRAT', 'RANASUG', 'RANEENGINE', 'RANEHOLDIN', 'RATEGAIN', 'RATNAMANI',
            'RATNAVEER', 'RAYMOND', 'RBA', 'RBL', 'RBLBANK', 'RCF',
            'RCOM', 'RECLTD', 'REDINGTON', 'REDTAPE', 'REFEX', 'REGENCERAM',
            'RELAXO', 'RELCHEMQ', 'RELIANCE', 'RELIGARE', 'RELINFRA', 'REMSONSIND',
            'RENUKA', 'REPCOHOME', 'REPL', 'REPRO', 'RESPONIND', 'RGL',
            'RHFL', 'RHIM', 'RHL', 'RICOAUTO', 'RIIL', 'RISHABH',
            'RITCO', 'RITES', 'RKDL', 'RKEC', 'RKFORGE', 'RMCL',
            'RML', 'ROHLTD', 'ROLEXRINGS', 'ROLLT', 'ROLTA', 'ROML',
            'ROSSARI', 'ROSSELLIND', 'ROTO', 'ROUTE', 'RPGLIFE', 'RPOWER',
            'RPPINFRA', 'RPPL', 'RPSGVENT', 'RRKABEL', 'RSSOFTWARE', 'RSWM',
            'RSYSTEMS', 'RTNINDIA', 'RTNPOWER', 'RUBYMILLS', 'RUCHINFRA', 'RUCHIRA',
            'RUPA', 'RUSHIL', 'RUSTOMJEE', 'RVHL', 'RVNL', 'S&SPOWER',
            'SABEVENTS', 'SADBHAV', 'SADBHIN', 'SADHNANIQ', 'SAFARI', 'SAGARDEEP',
            'SAGCEM', 'SAH', 'SAHYADRI', 'SAIL', 'SAKAR', 'SAKHTISUG',
            'SAKSOFT', 'SAKUMA', 'SALASAR', 'SALONA', 'SALSTEEL', 'SALZERELEC',
            'SAMBHAAV', 'SAMHI', 'SAMPANN', 'SANCO', 'SANDESH', 'SANDHAR',
            'SANDUMA', 'SANGAMIND', 'SANGHIIND', 'SANGHVIMOV', 'SANGINITA', 'SANOFI',
            'SANSERA', 'SAPPHIRE', 'SARDAEN', 'SAREGAMA', 'SARLAPOLY', 'SARVESHWAR',
            'SASKEN', 'SASTASUNDR', 'SATIA', 'SATIN', 'SATINDLTD', 'SBC',
            'SBCL', 'SBFC', 'SBGLP', 'SBICARD', 'SBILIFE', 'SBIN',
            'SCHAEFFLER', 'SCHAND', 'SCHNEIDER', 'SCI', 'SCPL', 'SDBL',
            'SEAMECLTD', 'SECURCRED', 'SECURKLOUD', 'SEJALLTD', 'SELAN', 'SELMC',
            'SEMAC', 'SENCO', 'SEPC', 'SEQUENT', 'SERVOTECH', 'SESHAPAPER',
            'SETCO', 'SEYAIND', 'SFL', 'SGIL', 'SGL', 'SHAH',
            'SHAHALLOYS', 'SHAILY', 'SHAKTIPUMP', 'SHALBY', 'SHALPAINTS', 'SHANKARA',
            'SHANTI', 'SHANTIGEAR', 'SHARDACROP', 'SHARDAMOTR', 'SHAREINDIA', 'SHEMAROO',
            'SHILPAMED', 'SHIVALIK', 'SHIVAMAUTO', 'SHIVAMILLS', 'SHIVATEX', 'SHK',
            'SHOPERSTOP', 'SHRADHA', 'SHREDIGCEM', 'SHREECEM', 'SHREEPUSHK', 'SHREERAMA',
            'SHRENIK', 'SHREYANIND', 'SHREYAS', 'SHRIPISTON', 'SHRIRAMFIN', 'SHRIRAMPPS',
            'SHYAMCENT', 'SHYAMMETL', 'SHYAMTEL', 'SICALLOG', 'SIEMENS', 'SIGACHI',
            'SIGIND', 'SIGMA', 'SIGNATURE', 'SIKKO', 'SIL', 'SILGO',
            'SILINV', 'SILLYMONKS', 'SILVERTUC', 'SIMBHALS', 'SIMPLEXINF', 'SINDHUTRAD',
            'SINTERCOM', 'SIRCA', 'SIS', 'SITINET', 'SIYSIL', 'SJS',
            'SJVN', 'SKFINDIA', 'SKIPPER', 'SKMEGGPROD', 'SKYGOLD', 'SMARTLINK',
            'SMCGLOBAL', 'SMLISUZU', 'SMLT', 'SMSLIFE', 'SMSPHARMA', 'SNOWMAN',
            'SOBHA', 'SOFTTECH', 'SOLARA', 'SOLARINDS', 'SOMANYCERA', 'SOMATEX',
            'SOMICONVEY', 'SONACOMS', 'SONAMCLOCK', 'SONATSOFTW', 'SOTL', 'SOUTHBANK',
            'SOUTHWEST', 'SPAL', 'SPANDANA', 'SPARC', 'SPCENET', 'SPECIALITY',
            'SPENCERS', 'SPENTEX', 'SPIC', 'SPLIL', 'SPLPETRO', 'SPMLINFRA',
            'SPORTKING', 'SPYL', 'SREEL', 'SRF', 'SRGHFL', 'SRHHYPOLTD',
            'SRPL', 'SSWL', 'STAR', 'STARCEMENT', 'STARHEALTH', 'STARPAPER',
            'STARTECK', 'STCINDIA', 'STEELCAS', 'STEELCITY', 'STEELXIND', 'STEL',
            'STERTOOLS', 'STLTECH', 'STOVEKRAFT', 'STYLAMIND', 'STYRENIX', 'SUBEXLTD',
            'SUBROS', 'SUDARSCHEM', 'SUKHJITS', 'SULA', 'SUMICHEM', 'SUMIT',
            'SUMMITSEC', 'SUNDARAM', 'SUNDARMFIN', 'SUNDARMHLD', 'SUNDRMBRAK', 'SUNDRMFAST',
            'SUNFLAG', 'SUNPHARMA', 'SUNTECK', 'SUNTV', 'SUPERHOUSE', 'SUPERSPIN',
            'SUPRAJIT', 'SUPREMEENG', 'SUPREMEIND', 'SUPREMEINF', 'SUPRIYA', 'SURANASOL',
            'SURANAT&P', 'SURYALAXMI', 'SURYAROSNI', 'SURYODAY', 'SUTLEJTEX', 'SUULD',
            'SUVEN', 'SUVENPHAR', 'SUVIDHAA', 'SUZLON', 'SVLL', 'SVPGLOB',
            'SWANENERGY', 'SWARAJENG', 'SWELECTES', 'SWSOLAR', 'SYMPHONY', 'SYNCOMF',
            'SYNGENE', 'SYRMA', 'TAINWALCHM', 'TAJGVK', 'TAKE', 'TALBROAUTO',
            'TANLA', 'TARAPUR', 'TARC', 'TARMAT', 'TARSONS', 'TASTYBITE',
            'TATACHEM', 'TATACOFFEE', 'TATACOMM', 'TATACONSUM', 'TATAELXSI', 'TATAINVEST',
            'TATAMETALI', 'TATAMOTORS', 'TATAMTRDVR', 'TATAPOWER', 'TATASTEEL', 'TATASTLLP',
            'TATVA', 'TBZ', 'TCI', 'TCIEXP', 'TCNSBRANDS', 'TCPLPACK',
            'TCS', 'TDPOWERSYS', 'TEAMLEASE', 'TECHIN', 'TECHM', 'TECHNOE',
            'TECILCHEM', 'TEGA', 'TEJASNET', 'TEMBO', 'TERASOFT', 'TEXINFRA',
            'TEXMOPIPES', 'TEXRAIL', 'TFCILTD', 'TFL', 'TGBHOTELS', 'THANGAMAYL',
            'THEINVEST', 'THEJO', 'THEMISMED', 'THERMAX', 'THOMASCOOK', 'THOMASCOTT',
            'THYROCARE', 'TI', 'TIDEWATER', 'TIIL', 'TIINDIA', 'TIJARIA',
            'TIL', 'TIMESGTY', 'TIMETECHNO', 'TIMKEN', 'TINPLATE', 'TIPSFILMS',
            'TIPSINDLTD', 'TIRUMALCHM', 'TIRUPATIFL', 'TITAGARH', 'TITAN', 'TMB',
            'TNPETRO', 'TNPL', 'TNTELE', 'TOKYOPLAST', 'TORNTPHARM', 'TORNTPOWER',
            'TOTAL', 'TOUCHWOOD', 'TPLPLASTEH', 'TRACXN', 'TREEHOUSE', 'TREJHARA',
            'TREL', 'TRENT', 'TRF', 'TRIDENT', 'TRIGYN', 'TRIL',
            'TRITURBINE', 'TRIVENI', 'TRU', 'TTKHLTCARE', 'TTKPRESTIG', 'TTL',
            'TTML', 'TV18BRDCST', 'TVSELECT', 'TVSHLTD', 'TVSMOTOR', 'TVSSCS',
            'TVSSRICHAK', 'TVTODAY', 'TVVISION', 'UBL', 'UCAL', 'UCOBANK',
            'UDAICEMENT', 'UDS', 'UFLEX', 'UFO', 'UGARSUGAR', 'UGROCAP',
            'UJAAS', 'UJJIVAN', 'UJJIVANSFB', 'ULTRACEMCO', 'UMAEXPORTS', 'UMANGDAIRY',
            'UMESLTD', 'UNICHEMLAB', 'UNIDT', 'UNIENTER', 'UNIINFO', 'UNIONBANK',
            'UNIPARTS', 'UNITECH', 'UNITEDPOLY', 'UNITEDTEA', 'UNIVASTU', 'UNIVCABLES',
            'UNIVPHOTO', 'UNOMINDA', 'UPL', 'URAVI', 'URJA', 'USHAMART',
            'USK', 'UTIAMC', 'UTKARSHBNK', 'UTTAMSUGAR', 'V2RETAIL', 'VADILALIND',
            'VAIBHAVGBL', 'VAISHALI', 'VAKRANGEE', 'VALIANTLAB', 'VALIANTORG', 'VARDHACRLC',
            'VARDMNPOLY', 'VARROC', 'VASCONEQ', 'VASWANI', 'VBL', 'VCL',
            'VEDL', 'VENKEYS', 'VENUSPIPES', 'VENUSREM', 'VERANDA', 'VERTOZ',
            'VESUVIUS', 'VETO', 'VGUARD', 'VHL', 'VICEROY', 'VIDHIING',
            'VIJAYA', 'VIJIFIN', 'VIKASECO', 'VIKASLIFE', 'VIMTALABS', 'VINATIORGA',
            'VINDHYATEL', 'VINEETLAB', 'VINNY', 'VINYLINDIA', 'VIPCLOTHNG', 'VIPIND',
            'VIPULLTD', 'VIRINCHI', 'VISAKAIND', 'VISESHINFO', 'VISHAL', 'VISHNU',
            'VISHWARAJ', 'VIVIDHA', 'VLEGOV', 'VLSFINANCE', 'VMART', 'VOLTAMP',
            'VOLTAS', 'VPRPL', 'VRLLOG', 'VSSL', 'VSTIND', 'VSTTILLERS',
            'VTL', 'WABAG', 'WALCHANNAG', 'WANBURY', 'WATERBASE', 'WEALTH',
            'WEBELSOLAR', 'WEIZMANIND', 'WEL', 'WELCORP', 'WELENT', 'WELINV',
            'WELSPUNIND', 'WENDT', 'WESTLIFE', 'WEWIN', 'WHEELS', 'WHIRLPOOL',
            'WILLAMAGOR', 'WINDLAS', 'WINDMACHIN', 'WINSOME', 'WIPL', 'WIPRO',
            'WOCKPHARMA', 'WONDERLA', 'WORTH', 'WSI', 'WSTCSTPAPR', 'XCHANGING',
            'XELPMOC', 'XPROINDIA', 'YAARI', 'YASHO', 'YATHARTH', 'YATRA',
            'YESBANK', 'YUKEN', 'ZAGGLE', 'ZEEL', 'ZEELEARN', 'ZEEMEDIA',
            'ZENITHEXPO', 'ZENITHSTL', 'ZENSARTECH', 'ZENTEC', 'ZFCVINDIA', 'ZIMLAB',
            'ZODIAC', 'ZODIACLOTH', 'ZOMATO', 'ZOTA', 'ZUARI', 'ZUARIIND',
            'ZYDUSLIFE', 'ZYDUSWELL'
                ]
    
    return SYMBOLS

@st.cache_data(show_spinner=False )
def getDataOptimized(interval='1mo',symbolsList=getSymbols()):
    print(len(symbolsList))
    intervals=['1m', '5m', '15m', '30m', '90m', '1h', '1d', '1wk', '1mo', '3mo']
    periods=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if interval not in intervals:
        raise Exception(f'interval argument is not valid!!\n{intervals}')
    periodMapping={
                  '1m':'5d',
                  '5m':'5d',
                  '15m':'60d',
                  '30m':'60d',
                  '90m':'60d',
                  '1h':'520d',
                  '1d':'5y',
                  '1wk':'10y',
                  '1mo':'ytd',
                  '3mo':'max'
                  }
    STOCK_DATA={}
    if interval in intervals:
        period=periodMapping[interval]
    else:
        raise Exception(f'Error in selecting Interval and Period\nInterval can be within: {intervals}')
    
    SYMBOLS=[f'{i}.NS' for i in symbolsList]
    try:
        DATA=yf.download(SYMBOLS,interval=interval,period=period,threads = True)
    except Exception as e:
        #print(f'Error in getting {interval} data of stock {s}\n','-'*100)
        print(e)
    for s in SYMBOLS:
        try:
            data=DATA.T.swaplevel().T[s]
            data.dropna(subset=['Close','Open','High','Low'],axis=0,inplace=True)
            STOCK_DATA[s.replace('.NS','')]=data #.rstrip('.NS')
        except Exception as e:
            print(f'Error in getting data of stock {s}\n')
            print(e,'-'*100)

    return STOCK_DATA

@st.cache_data(show_spinner=False )
def getData(interval='1mo',period='10y',symbolsList=getSymbols()):
    print('No of symbols: ',len(symbolsList))
    intervals=['1m', '5m', '15m', '30m', '90m', '1h', '1d', '1wk', '1mo', '3mo']
    periods=['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if interval not in intervals:
        raise Exception(f'interval argument is not valid!!\n{intervals}')
    if period not in periods:
        raise Exception(f'period argument is not valid!!\n{periods}')
    
    
    with st.spinner(f'Getting data for all {len(symbolsList)} stocks!!'):
        STOCK_DATA={}
        SYMBOLS=[f'{i}.NS' for i in symbolsList]
        try:
            DATA=yf.download(SYMBOLS,interval=interval,period=period,threads = True)
        except Exception as e:
            #print(f'Error in getting {interval} data of stock {s}\n','-'*100)
            print(e)
        
        for s in SYMBOLS:
            try:
                data=DATA.T.swaplevel().T[s]
                data.dropna(subset=['Close','Open','High','Low'],axis=0,inplace=True)
                STOCK_DATA[s.replace('.NS','')]=data #.rstrip('.NS')
            except Exception as e:
                print(f'Error in getting data of stock {s}\n')
                print(e,'-'*100)

    return STOCK_DATA

#Functions
def constrictData(STOCK_DATA,n=1300):
    DATA=deepcopy(STOCK_DATA)
    for s,d in DATA.items():
        DATA[s]=d.tail(n)
    return DATA

@st.cache_resource
def download_file(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False)


# New Candle detection with separate percentage for leg out and legin candle
def detectExcitingBaseCandle(data,legInPercent=0.4,legOutPercent=0.6,basePercent=0.5):
    data['Body']=data['Close']-data['Open']
    data['Range']=data['High']-data['Low']
    data['Type']=np.where(data['Close']>=data['Open'],'Bullish','Bearish')
    data['LegInCandle']=np.where(((data['Body'].abs()/data['Range'])>=legInPercent),True,False)
    data['BaseCandle']=np.where((data['Body'].abs()/data['Range'])<basePercent,True,False)
    data['LegOutCandle']=np.where(((data['Body'].abs()/data['Range'])>=legOutPercent),True,False)
    return data

def detectDemandZones(data,setup=['dbr']):
    if type(setup)!=list:
        print('setup argument needs to be list')
        return None
    data['DemandZone']=False
    
    for s in setup:

        if s.upper() == 'BR':
            data['DemandZone']=np.where(data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                          &(data['Type'].shift(-1)=='Bullish')
                                          ,(data['DemandZone']|True),(data['DemandZone']|False))
            
        if s.upper() == 'BRR':
            data['DemandZone']=np.where(data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)&
                                      data['LegInCandle'].shift(-2)
                                      &(data['Type'].shift(-1)=='Bullish')
                                          &(data['Type'].shift(-2)=='Bullish')
                                          ,(data['DemandZone']|True),(data['DemandZone']|False))

        elif s.upper() == 'DBR':
            data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bearish')&(data['Type'].shift(-1)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        elif s.upper() == 'RBR':
            data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bullish')&(data['Type'].shift(-1)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        
        elif s.upper() == 'RBRR':
            data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bullish')&(data['Type'].shift(-1)=='Bullish')&
                                       (data['Type'].shift(-2)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))

        elif s.upper() == 'RRBRR':
             data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bullish')&(data['Type'].shift(-1)=='Bullish'))&
                                      ((data['Type'].shift(2)=='Bullish')&(data['Type'].shift(-2)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))

        elif s.upper() == 'DBRR':
            data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bearish')&(data['Type'].shift(-1)=='Bullish')&
                                       (data['Type'].shift(-2)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))

        elif s.upper() == 'DDBRR':
             data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bearish')&(data['Type'].shift(-1)=='Bullish'))&
                                      ((data['Type'].shift(2)=='Bearish')&(data['Type'].shift(-2)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        elif s.upper() == 'DBBR':
             data['DemandZone']=np.where(data['LegInCandle'].shift(2)&
                                    
                                      ((data['Type'].shift(2)=='Bearish')&(data['Type'].shift(-1)=='Bullish'))&
                                      data['BaseCandle'].shift(1)&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        
        elif s.upper() == 'RBBR':
             data['DemandZone']=np.where(data['LegInCandle'].shift(2)&
                                    
                                      ((data['Type'].shift(2)=='Bullish')&(data['Type'].shift(-1)=='Bullish'))&
                                      data['BaseCandle'].shift(1)&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        elif s.upper() == 'DBRRR':
            data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bearish')&(data['Type'].shift(-1)=='Bullish')&
                                       (data['Type'].shift(-2)=='Bullish')&(data['Type'].shift(-3)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)&data['LegOutCandle'].shift(-2)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        elif s.upper() == 'RBRRR':
            data['DemandZone']=np.where(data['LegInCandle'].shift(1)&
                                      ((data['Type'].shift(1)=='Bullish')&(data['Type'].shift(-1)=='Bullish')&
                                       (data['Type'].shift(-2)=='Bullish')&(data['Type'].shift(-3)=='Bullish'))&
                                      data['BaseCandle']&
                                      data['LegOutCandle'].shift(-1)&data['LegOutCandle'].shift(-2)
                                      ,(data['DemandZone']|True),(data['DemandZone']|False))
        
    return data
    
def getDemandZones(data,testedLimit=1,testedBy='Low',testedLine='max',noOfZones=0,PL_HighLow=False):
    zones={}
    
    if testedBy.lower() not in ['low','close','open','high']:
        raise Exception('TestedBy must be within Low/Close/Open')
    else:
        if testedBy.capitalize()=='Low':
            testedBy1=testedBy.capitalize()
            testedBy2=testedBy.capitalize()
        elif testedBy.capitalize() in ['Close','Open']:
            testedBy1='Close'
            testedBy2='Open'
        else:
            testedBy1='Low'
            testedBy2='Low'
            print('testedBy is invalid!!\nTaking testedBy="Low"')
        
    if ('MAX' in testedLine.upper()) or ('PL' in testedLine.upper()):
        func=max
    elif ('MIN' in testedLine.upper()) or ('DL' in testedLine.upper()):
        func=min
    else:
        raise Exception('TestedLine must be within max/min or PL,DL')
        
    flag=False
    doubleBasePattern=False
    
    try:
        index=data[data['DemandZone']].index
    except:
        print("Error: Cant get the DemandZone column from data\nRun functions:\n \
        1)detectExcitingBaseCandle\n2)detectDemandZoneZones")
    if (noOfZones is not None) or noOfZones!=0:
        index=index[-noOfZones:]
    #print(index,'#'*50,sep='\n')
    zonesTested={}
    prev,doublePrev=0,0
    for i,r in data.iterrows():
        for d,(pl,dl) in zones.items():
            if min(r[testedBy1],r[testedBy2])<=func(pl,dl):
                #print(f'The zone of {d} - ({pl},{dl}) was tested on {str(i)} with\nlow of {r.Low}\nclose of {r.Close}')
                #print('-'*30)
                if d in zonesTested.keys():
                    zonesTested[d]=zonesTested[d]+1
                else:
                    zonesTested[d]=1
                
        if flag:
            flag=False
            if PL_HighLow:
                if r.Type=='Bullish':
                    PL=base.High
                    if prev.Type=='Bearish':
                        DL=min(prev.Low,base.Low,r.Low)
                    else:
                        DL=min(base.Low,r.Low)
                    
                else:
                    print("ERROR!!")
                    raise Exception('Its not in Bullish condition! Look into code')
 
            else:
                if r.Type=='Bullish':
                    PL=max(base.Close,base.Open)
                    if prev.Type=='Bearish':
                        DL=min(prev.Low,base.Low,r.Low)
                    else:
                        DL=min(base.Low,r.Low)
                else:
                    print("ERROR!!")
                    raise Exception('Its not in Bullish condition! Look into code')
                    
            zones[base_date]=(PL,DL)
        
        if doubleBasePattern:
            doubleBasePattern=False
            if PL_HighLow:
                if r.Type=='Bullish':
                    PL=max(base1.High,base2.High)
                    if doublePrev.Type=='Bearish':
                        DL=min(doublePrev.Low,base1.Low,base2.Low,r.Low)
                    else:
                        DL=min(base1.Low,base2.Low,r.Low)
                    
                else:
                    print("ERROR!!")
                    raise Exception('Its not in Bullish condition! Look into code')
 
            else:
                if r.Type=='Bullish':
                    PL=max(base1.Close,base1.Open,base2.Close,base2.Open)
                    if doublePrev.Type=='Bearish':
                        DL=min(doublePrev.Low,base1.Low,base2.Low,r.Low)
                    else:
                        DL=min(base1.Low,base2.Low,r.Low)
                else:
                    print("ERROR!!")
                    raise Exception('Its not in Bullish condition! Look into code')
                    
            zones[base_date]=(PL,DL)

        if i in index:      
            if prev.BaseCandle and not prev.LegInCandle and not prev.LegOutCandle:
                doubleBasePattern=True
                drop=doublePrev
                base1=prev
                base2=r
                base_date=str(i)
                #print(base_date,'Double Base')
                continue
                
            flag=True
            drop=prev
            base=r
            base_date=str(i)
            continue
            
        doublePrev=prev    
        prev=r   
        
    for d,c in zonesTested.items():
        if c>testedLimit:
            #print(f'The Zone on date {d} with zone {zones[d]} was tested {c} times!\n','-'*100)
            del zones[d]
    return zones

def DEMANDZONES(Data,TestLimit=1,TestedBy='Low',TestedLine='max',Setup=['dbr','dbbr','rbr','rbbr','dbrr'],LegInCandlePercent=0.4,LegOutCandlePercent=0.7,BaseCandlePercent=0.3,noOfZones=0,HighLowZoneMarking=False):
    data=Data.copy()
    data=detectExcitingBaseCandle(data,legInPercent=LegInCandlePercent,legOutPercent=LegOutCandlePercent,basePercent=BaseCandlePercent)
    data=detectDemandZones(data,setup=Setup)
    zones=getDemandZones(data,testedLimit=TestLimit,testedBy=TestedBy,testedLine=TestedLine,noOfZones=noOfZones,PL_HighLow=HighLowZoneMarking)
    return (data,zones)

def getNearestZones(data,testLimit=1,closeTo='min',setup=['dbr','dbbr','rbr','rbbr','dbrr'],variance=2,testedBy='Low',testedLine='max',value='Close',legInCandlePercent=0.4,legOutCandlePercent=0.6,
                               baseCandlePercent=0.5,highlowMarking=False,noOfZones=0):
    DATA=deepcopy(data)
    sd_dict={}
    price_dict={}
    SDZONES_WATCHLIST={}
    
    if ('MAX' in closeTo.upper()) or ('PL' in closeTo.upper()):
        getLine=max
    elif ('MIN' in closeTo.upper()) or ('DL' in closeTo.upper()):
        getLine=min
    elif ('MEAN' in closeTo.upper()) or ('AV' in closeTo.upper()):
        def getLine(i,j):
            return round((i+j)/2,2)
    else:
        raise Exception('TestedLine must be within max/min or PL,DL')
    
    print(f'Getting zones for all {len(DATA)} stocks!!!')   
    with st.spinner(f'Getting zones for all {len(DATA)} stocks!, please wait...'):
        for i,(s,d) in enumerate(DATA.items()):
            # print(s)
            _,zones=DEMANDZONES(d.iloc[:-1],TestLimit=testLimit,Setup=setup,LegInCandlePercent=legInCandlePercent,LegOutCandlePercent=legOutCandlePercent,
                                BaseCandlePercent=baseCandlePercent,noOfZones=noOfZones,TestedBy=testedBy,TestedLine=testedLine,HighLowZoneMarking=highlowMarking)
            sd_dict[s]=zones
            if len(d[value])<3:
                price_dict[s]=0
            else:
                price_dict[s]=d[value].iloc[-1]
    sleep(2)
    print('Zones gathered ,filtering as per requirement\n')
    with st.spinner('Getting nearest zones...'):
        for s,sdzones in sd_dict.items():
            # print(price_dict[s],sdzones)
            width=(price_dict[s]*variance)/100

            if sdzones is None:
                print(f'{s} skipped no SDZones')
                continue
            
            for d,(i,j) in sdzones.items():
                
                if width>=(price_dict[s]-getLine(i,j)) and ((price_dict[s]-getLine(i,j))>0):
                    #if width>=abs(price_dict[s]-min(i,j)): #Have removed abs for getting only high values
                    SDZONES_WATCHLIST[s]=((min(i,j),max(i,j)),price_dict[s],d.split(" ")[0],d.split(" ")[1])
            # print(f'{s} is done')

    if len(SDZONES_WATCHLIST)==0:
        return None
    SDZONES_WATCHLIST=dict(sorted(SDZONES_WATCHLIST.items(), key=lambda item: item[1]))
    remove_list=[]
    for i,((j),p,d,t) in SDZONES_WATCHLIST.items():
        if (DATA[i].iloc[-1].Low<=max(j[0],j[1])):
            
            if (DATA[i].iloc[-1].Close<=max(j[0],j[1])) and (DATA[i].iloc[-1].Low>=min(j[0],j[1])):
                print(i,'Close and Low less than Max')
                continue
            else:
                remove_list.append(i)
                continue
            
        print(i,f'({round(j[0],2)},{round(j[1],2)})',round(p,2),d,t,sep=' -> ')
    
    for i in remove_list:
        print(i)
        del SDZONES_WATCHLIST[i]    
        #print(i,f'({round(j[0],2)},{round(j[1],2)})',round(p,2),d,t,sep=' -> ')
    print('\nNo of Stocks with demand zones: ',len(SDZONES_WATCHLIST))
    print('='*80)
    return SDZONES_WATCHLIST



with col1:

    TIMEFRAME=st.selectbox("TimeFrame of Data: ",['1m', '5m', '15m', '30m', '90m','1h', '1d', '1wk', '1mo', '3mo'][::-1])
    PERIOD=st.selectbox("Period of Data: ",['1d', '5d', '1mo', '3mo', '6mo','1y', '2y', '5y', '10y', 'ytd', 'max'][::-1])
    TESTLIMIT=st.number_input('Allowed number of times zones tested: ',min_value=0,max_value=20,step=1,value=1)
    VARIANCE=st.number_input('Enter Price Variance value: ',min_value=0.0,max_value=100.0,value=5.0,step=0.5)
    
    
with col2:
    SETUP=st.multiselect("Demand Zones Setup: ",
                    ['DBR','RBR','DBRR','DDBRR','RBRR','RRBRR','DBBR','RBBR'],default=['DBR','RBR'])
    LEGINCANDLEPERCENT=st.number_input('Enter LegIn Candle Percentage',min_value=0.0,max_value=1.0,value=0.4,step=0.05)
    BASECANDLEPERCENT=st.number_input('Enter Base Candle Percentage',min_value=0.0,max_value=1.0,value=0.5,step=0.05)
    LEGOUTCANDLEPERCENT=st.number_input('Enter LegOut Candle Percentage',min_value=0.0,max_value=1.0,value=0.6,step=0.05)
    # DOWNLOAD=st.checkbox('Download the file: ',value=False)
    
with st.sidebar:
    MARKING=st.radio('Marking Type: ',['Normal','HighLow'])
    if MARKING=='HighLow':
        MARKING=True
    else:
        MARKING=False
    TESTEDBY=st.selectbox('Select value that is testing the zone: ',['Low','Open','Close','High'])
    TESTEDLINE=st.selectbox('Select line that is tested(MAX[PL]/MIN[DL]): ',['MAX','MIN','PL','DL'])
    CLOSETO=st.selectbox('Current price closest to(MAX[PL]/MIN[DL]/MEAN[AVG]): ',['MIN','MAX','MEAN'])
    RECENTZONES=st.number_input('No Of recent zones to consider: ',min_value=0,max_value=100,value=0,step=1)

GetZones=st.button('Get Zones')
Clear=st.button('Clear')

def getZones():
    if (TIMEFRAME and PERIOD and SETUP and MARKING and TESTLIMIT and VARIANCE and LEGINCANDLEPERCENT and 
        BASECANDLEPERCENT and LEGOUTCANDLEPERCENT and RECENTZONES and TESTEDBY and 
        TESTEDLINE and CLOSETO) is not None:
        
        DATA=getData(interval=TIMEFRAME,period=PERIOD,symbolsList=getSymbols())
        if len(DATA)>5:
            Data=deepcopy(DATA)
        else:
            st.error('ERROR: No data!!')
            
        DZonesList=getNearestZones(Data,testLimit=TESTLIMIT,closeTo=CLOSETO,setup=SETUP,variance=VARIANCE,
                        testedBy=TESTEDBY,testedLine=TESTEDLINE,value='Close',legInCandlePercent=LEGINCANDLEPERCENT,
                        legOutCandlePercent=LEGOUTCANDLEPERCENT,baseCandlePercent=BASECANDLEPERCENT,highlowMarking=MARKING,
                        noOfZones=RECENTZONES)
        
        if DZonesList is None:
            return None
        
        df=pd.DataFrame(DZonesList).T
        df=df.reset_index().rename({'index':'Symbol',0:'Zones',1:'Price',2:'Date',3:'Time'},axis=1)
        df['Price']=df['Price'].astype('float').round(1)
        return df
    else:
        st.error('Enter all the configurations!!')

if GetZones:
    DZONES=getZones()
    
    if (DZONES is None):
        status=st.warning('There is no Zones found!\nTry different configs')
    else:
        status=st.success(f'There are {len(DZONES)} demand zones')
        table=st.dataframe(DZONES,width=1000,height=500)
   
        
        # csv = download_file(DZONES)
        # col2.download_button(
        #     label="Download data as CSV",
        #     data=csv,
        #     file_name=f"{TIMEFRAME}_Demand_Zones_{str(int((LEGINCANDLEPERCENT)*100))}{str(int((BASECANDLEPERCENT)*100))}{str(int((LEGOUTCANDLEPERCENT)*100))}_{str(datetime.today().date()).replace('-','_')}.csv",
        #     mime='text/csv',
        # )
        col2.download_button(
            label="Download data as CSV",
            data=DZONES.to_csv(index=False),
            file_name=f"{TIMEFRAME}_Demand_Zones_{str(int((LEGINCANDLEPERCENT)*100))}{str(int((BASECANDLEPERCENT)*100))}{str(int((LEGOUTCANDLEPERCENT)*100))}_{str(datetime.today().date()).replace('-','_')}.csv",
            mime='text/csv',
        )



if Clear:
    status=st.empty()
    GetZones=False   
        
        
        

