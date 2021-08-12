import numpy as np
from flask import Flask, request
from Evolver2048 import Genome, Fitness

app = Flask(__name__)

def chooseAction(actions, board):
	# This is where we pick the action
	# actions is a 4-element array of booleans, corresponding to whether the corresponding action is allowed
	# board is a 4x4 nested list containing the tile values
	board = np.array(board)
	return Fitness.modelChooseAction(actions, board, model)

@app.route("/")
def hello_world():
	return "Hello, World!"

@app.route("/action", methods=["POST"])
def action():
	# Read json from the request
	response = request.get_json()
	# Choose the first valid action
	action = chooseAction(**response)
	# Return chosen action
	return str(action)

# hehe
genome = Genome.fromArray(np.array([-1.788212566243333, 0.886403900378762, -0.23750841603079392, 0.37839920867611687, 0.9009008495022475, -0.25007767355140254, 1.5250342904570044, 0.6939401180387702, 0.01279251921471658, -0.23219604868894986, 0.7798146947114021, -0.7356424252061731, -2.2615516227459964, -3.1450427202932114, -0.3736065298574518, -0.7722817074285016, 0.2973669368132523, 0.44628992064386996, 0.0649938660071483, 3.2146999789070043, -0.7049780342231385, -0.5375444795660731, -0.784761519567263, 0.27561633629739357, 2.7511687760004326, 0.5832556873273089, 0.7533747837157727, 1.8916784795863157, 0.8653137081836695, -3.762425537941483, -0.5992129784804734, -1.4453299993863618, -1.9154186904757218, -0.21478422914905915, 0.41029857479749815, 0.8951395222749576, 0.6785586621285047, 1.5979518151746614, 1.5494328887702582, -0.804368612433364, -0.1220898127522243, 2.489502618376311, -0.9064428430768487, -0.8718936208640625, 0.9346961471902597, -0.9397664873205658, -0.5059096142502069, 0.4460044154470093, 0.9165200676970704, -1.01098115545326, 0.5593048949619652, 1.3546777567452617, -1.4996640004210886, -0.23220067861793225, -1.4008200506486574, -0.11917702475478475, 0.8214562851739071, -0.0018134171480370664, -0.11332030672961446, 1.8762033669052631, -0.41892914287797245, -0.2733315342807772, 0.08242562390375863, -0.9172767168132452, -1.0592200230289581, -0.9086240147506548, -0.4590452242793658, 1.1075013126090618, 0.3072622592770241, 0.039674944960337744, -0.1534588996801891, 2.342221544680733, -0.09794978147765385, 1.4999109583065193, -0.5550184435075477, -0.30283432693335866, 0.8042294262611124, 1.3178026265691312, -1.7821061999847145, 0.07566691829170269, -1.2450687338856057, 1.2947816912574188, -0.8442143501374009, 0.217433137541792, -1.372032382246656, -0.4269883484025515, -0.02326294798233, -0.23365416253905164, 4.102130931027755, 0.28024897103408564, -0.4413561556669543, 1.0153323913290915, -0.4802405928339185, 2.767066015379591, 0.5048263901077314, 0.9370557640102208, 0.47006600196801307, 0.24015708847574935, -5.394735549989624, 0.45354265637238766, -0.087305533848415, -1.0930373240684452, -0.5761205567307435, 0.1271804556246181, 3.2741038018662536, 0.4057377849522287, -1.2552028199610201, -1.1809749566586047, 0.032987848850195345, 2.144328537143822, -0.8665064627031944, 0.8908659430619228, -0.2884317774855687, -0.5450883183972953, 1.3186599603510163, 0.9636592757387579, -2.029721903991897, -1.8599727533213888, 0.000506664743871954, 0.2659035883575452, -0.7209137610922541, -0.5050286567851037, 2.30594789559643, 1.2849768087003337, 0.3558615784014594, 1.0104080739832682, 0.04164481073242521, 0.7909631252342565, 0.4333649589277728, -1.4683786114261113, -0.07994162502046775, -0.23243596885007412, -1.2542005072878442, -0.18418691031196865, 1.797311704970831, 0.09280300192790805, 3.575533521176512, 0.13718333415580097, -0.6270323898080108, 1.5858368576710649, 0.4090536167455312, 0.8224121468357946, -0.3746804250434552, 0.39127816279287164, 0.8520951280408302, 2.1538226948104633, 0.18128158457648813, -0.9789832534777806, -0.16797180842406415, 0.6076954716954357, -0.0540985912110965, -0.6529746085370185, 0.3912906737549924, -0.20586168191762866, 0.9752613925949406, 0.029093019170274292, 0.7158149877629756, -0.9866631193608435, 1.4552808465243952, -1.6245884774898514, 1.1590184483785948, -0.46858278371540985, 0.6335241022021729, 0.6042386394886271, -1.2206727624487903, 3.0237575536134162, 0.3317911101892812, 0.2588657088966593, 0.29964897033605786, 0.4353631387040828, -0.44172742001809073, 1.1947873474214354]))
model = genome.toModel()

app.run(host="127.0.0.1", port=2048)