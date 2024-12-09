from hospital.models.Paciente import Paciente, TokenPaciente, create_patient
from hospital.models.Medico import Medico, TokenMedico, create_doctor
from hospital.api import *
from os import environ

frontend = APIRouter(
    prefix="/dapp",
)

graphql_server = environ["GRAPHQL_SERVER_URL"]

@frontend.post("/authenticate", tags=["Debugging"])
def authenticate_transaction(auth: Autenticacao):
    return authenticate(auth)

@frontend.get("/blockchain", tags=["Debugging"])
def get_blockchain():
    import requests
    import json
    
    response = requests.post(graphql_server, json={"query": "query notices { notices { edges { node { index input { index } payload } } } }"})
    data = response.json()

    for node in data["data"]["notices"]["edges"]:
        node["node"]["payload"] = json.loads(hex2str(node["node"]["payload"]))

    return data

@frontend.get("/appstate", tags=["Debugging"])
def get_appstate():
    from hospital.api.server import inspect
    app_state = inspect("/appstate")
    return app_state

@frontend.get("/pending_auths", tags=["Debugging"])
def get_pending_auths():
    from hospital.api.server import inspect
    app_state = inspect("/pending_auths")
    return app_state

@frontend.get("/valid_auths", tags=["Debugging"])
def get_valid_auths():
    from hospital.api.server import inspect
    app_state = inspect("/valid_auths")
    return app_state
    
@frontend.get("/access_tokens", tags=["Debugging"])
def get_access_tokens():
    from hospital.api.server import inspect
    app_state = inspect("/access_tokens")
    return app_state

@frontend.get("/allowed_reads", tags=["Debugging"])
def get_allowed_reads():
    from hospital.api.server import inspect
    app_state = inspect("/allowed_reads")
    return app_state

@frontend.post("/create_patient", tags=["Frontend"])
def create_patient_transaction(paciente: Paciente = Body(..., example={
        "nome": "João",
        "public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541734e56665a535961572f596947457852347848570a6a68703164494744687a4b4b51573935504562414741467643525876794d6131365a5479584e336b707132615753506761706e6c702b676d3350706e623958310a496763423644544148424e392f3156466c4951374f47534f6b513268394d70456558303367416845422b476d2b53626657303148612f6d704b784c33546b49430a374e39625a6378684d56743463516e4a742f452f6241584c4f335142774c4132302f4d4a39707a644d6952343555514754737641704a503230644a6d6b33414d0a30327455444a31575a43754a6e4563394c592b35506456755966546b6b616172437973334c594a72702b5a5a684268615358532f592f5139745967666b6439390a3373556e433139444174554b4c4f6f6b6d57664a672f50584b7a693647737872364f38384258336c4439584747344465414c4d4d3051327663496e762f446d490a6a774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
        "tipo_sanguineo": "A+",
        "peso": 80,
})):
    from hospital.api.server import advance

    payload = {
        "did": paciente.did,
        "method": "create_patient",
        "data": {
            "type": "patient",
            "attributes": paciente.model_dump()
        }
    }

    result = advance(payload)
    return result

@frontend.post("/create_doctor", tags=["Frontend"])
def create_doctor_transaction(medico: Medico = Body(..., example={
        "nome": "Cristiano",
        "public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b434151454177356d62483763474e524f50653648376a70574b0a3844646c386f7973503177504f6e3752696f34346e706a716a49654f3955442f2b522b6d4866746b414866334d77753553633434393163696c744363705953450a42476361526f7873533943517077385238363157787a616a6453342b3771307a5346586234463561546845646343626967365a525a723879394f6c714b4d77780a70706b67583444424b7345414f6f7a2b57676d413871576d2f692b4c474e4e6b546975474c574d7467732f7348783056686273716446534a6c325a784433462b0a326b33714a324b4f4359674c65417747532f4f6d365662362f5759374f595346443071493649535958474f63316873454d7578633536444b74537046684f65760a514d4e38386e426d72726862472f7a4279705a4a675279453834683066427a64385351654744786c515235376b745a696a543049564e63646a7571367654767a0a65774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
        "especialidade": "Cardiologista",
        "crm": "CRM/DF 123456"
    })):
    from hospital.api.server import advance

    payload = {
        "did": medico.did,
        "method": "create_doctor",
        "data": {
            "type": "doctor",
            "attributes": medico.model_dump()
        }
    }

    result = advance(payload)
    return result

@frontend.post("/create_access_token", tags=["Frontend"])
@auth
def create_access_token_transaction(paciente: TokenPaciente = Body(..., example={
        "shared_data": "{\"laudo\": \"Paciente com febre\", \"doenca\": \"Gripe\"}",
        "minutes_to_expire": 2,
        "public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541734e56665a535961572f596947457852347848570a6a68703164494744687a4b4b51573935504562414741467643525876794d6131365a5479584e336b707132615753506761706e6c702b676d3350706e623958310a496763423644544148424e392f3156466c4951374f47534f6b513268394d70456558303367416845422b476d2b53626657303148612f6d704b784c33546b49430a374e39625a6378684d56743463516e4a742f452f6241584c4f335142774c4132302f4d4a39707a644d6952343555514754737641704a503230644a6d6b33414d0a30327455444a31575a43754a6e4563394c592b35506456755966546b6b616172437973334c594a72702b5a5a684268615358532f592f5139745967666b6439390a3373556e433139444174554b4c4f6f6b6d57664a672f50584b7a693647737872364f38384258336c4439584747344465414c4d4d3051327663496e762f446d490a6a774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
        "private_key": "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945765149424144414e42676b71686b6947397730424151454641415343424b63776767536a41674541416f4942415143773156396c4a687062396949590a5446486a4564614f476e563067594f484d6f704262336b38527341594157384a46652f49787258706c504a633365536d725a705a492b42716d65576e364362630a2b6d6476316655694277486f4e4d41634533332f56555755684473345a49365244614830796b52356654654143455148346162354a743962545564722b616b720a4576644f51674c733331746c7a4745785733687843636d333854397342637337644148417344625438776e326e4e30794a486a6c52415a4f7938436b6b2f62520a306d615463417a546131514d6e565a6b4b346d63527a30746a376b3931573568394f53527071734c4b7a6374676d756e356c6d454746704a644c396a394432310a69422b52333333657853634c58304d4331516f733669535a5a386d44383963724f4c6f617a47766f377a77466665555031635962674e344173777a52446139770a69652f384f59695041674d424141454367674541542b474466326a502f587a5a65417035373035756b72446e49434d6c62467872556858754f556c6f6d792b430a6e694d58743658304a546c5170707a69486c314c33547130744e4d6969452f35786c636a684d5374514a7254784c61586c6464455571534e6b774b4d30664f790a35316d324d4b4e7966554d5159446a62716f664836734d686f4e6676444a717954612f366f5a4a32536453344c2b7338654a527565766e4638743737484774630a437244744570443073735146356d6e6562666a4345766f585a462b4e39476542632b3374386f574959394a7a41646c5233386351344b684545305567334d316a0a384a4c2b70736772507161474b7647766d4d344233464b574b6f463068796d31525a734a6f79474449452f57586c34524855694e67664c2b54644462526968490a485177775a596d667a6761536848492b54435652662f64576976374967654e6352576c303343677534514b4267514476612f65496a356a6770716e62734e505a0a414d305641394d616f566b35327646613276327771724a694e514d7a32426d727676496c31774b396e415178334c38324649776f3343375250594a75436144720a4c715256326c775452436a575a4831524c664251714c6a443038584d724236345a6b4d4838436e334664664767532b4a594767395a7578302f7573716f736a750a6e4472365168774237577a35724368326f7352703330393055514b4267514339452f52327659656e465266727255536a54353949554e444245395365444961650a6d51704b4a4e7853543455542b2b79657362506334713865316948394872567a6c455046384c38476936505a682f746a434d3337423843686f6a384b393655380a43612f77775239465342427854374571756f4b426b6b73426c6e316d2b4f4457566b376e75507730435254385776376a785447332f6965536d4f5661425048330a616d306e3666425733774b4267465857463444574f724551443457373937657447646d57375842327545364e75456f69695346316b55363051746d72654569690a784a336359426371674461414e65316c6f48706c746b4d2b45697a784e736761694d426538505058552b7a4a536b5234653966764a59375074664b54497442700a6d553658512f525a3247704b6c6f6869442f307a6b554c41776638664c587165654761516e516e7a335559462b74764e7279316c366b3642416f4741416c71740a514930376b796b41457a386c43364f434b44525a5a51344b4a36326750336c49563450392b6b686a4c3879444e6261677471396233745a7274657362393052780a5535576279306b5230544f5150627475565348546c432b672b564838444c4e534c583036466e4b2f51616e73577376587443564f4b63626c364e4a51656c71340a774d6e6332676b43366546344b76335a6b4b447066546e4b4955544f666e596b7863707a343645436759454132577355344a6b6c30625042654f5971385243380a737a48456b4d49472b63444764774e4f676647543071775274726771696f68424870387a4148636d3973626439387865477863315039743054574e6e754e44520a567333504a59697255466645526f445638746e7730374c51706c6c534942562f35456c5276346e54733673664d727545664b6569755832712f6c4a76392b41430a6a4b5a7278794238367539397a464c635149344b4665733d0a2d2d2d2d2d454e442050524956415445204b45592d2d2d2d2d0a",
        "medico_public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b434151454177356d62483763474e524f50653648376a70574b0a3844646c386f7973503177504f6e3752696f34346e706a716a49654f3955442f2b522b6d4866746b414866334d77753553633434393163696c744363705953450a42476361526f7873533943517077385238363157787a616a6453342b3771307a5346586234463561546845646343626967365a525a723879394f6c714b4d77780a70706b67583444424b7345414f6f7a2b57676d413871576d2f692b4c474e4e6b546975474c574d7467732f7348783056686273716446534a6c325a784433462b0a326b33714a324b4f4359674c65417747532f4f6d365662362f5759374f595346443071493649535958474f63316873454d7578633536444b74537046684f65760a514d4e38386e426d72726862472f7a4279705a4a675279453834683066427a64385351654744786c515235376b745a696a543049564e63646a7571367654767a0a65774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a"
    })):
    from hospital.api.server import advance
    from hospital.models import Pessoa
    from hospital.api.wallet import encrypt_msg, Encryption, sym_encrypt

    import os
    import time
    import base64

    medico = Pessoa(nome="_", public_key=paciente.medico_public_key)
    key = os.urandom(32).hex()
    encrypted_data = sym_encrypt(data=paciente.shared_data, key=key)

    payload = {
        "did": paciente.did,
        "method": "create_access_token",
        "data": {
            "type": "share",
            "attributes": {
                "token": os.urandom(16).hex(),
                "patient_did": paciente.did,
                "patient_public_key": paciente.public_key,
                "doctor_did": medico.did,
                "doctor_public_key": medico.public_key,
                "shared_data": encrypted_data["encrypted_message"],
                "encrypted_iv": encrypt_msg(Encryption(message=encrypted_data["iv"], public_key=medico.public_key))["encrypted_message"],
                "encrypted_key": encrypt_msg(Encryption(message=key, public_key=medico.public_key))["encrypted_message"],
                "expires_at": time.time() + paciente.minutes_to_expire*60 # 2 minutes
            }
        }
    }

    result = advance(payload)
    return result

@frontend.post("/access_data", tags=["Frontend"])
@auth
def access_data_transaction(medico: TokenMedico = Body(..., example={
        "paciente_did": "did:key:f930ed9de791aade7367240f76cf0ab22cfca2d7b957a373214abd7703fc8054",
        "token": "<INSERT_TOKEN_ID>",
        "public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b434151454177356d62483763474e524f50653648376a70574b0a3844646c386f7973503177504f6e3752696f34346e706a716a49654f3955442f2b522b6d4866746b414866334d77753553633434393163696c744363705953450a42476361526f7873533943517077385238363157787a616a6453342b3771307a5346586234463561546845646343626967365a525a723879394f6c714b4d77780a70706b67583444424b7345414f6f7a2b57676d413871576d2f692b4c474e4e6b546975474c574d7467732f7348783056686273716446534a6c325a784433462b0a326b33714a324b4f4359674c65417747532f4f6d365662362f5759374f595346443071493649535958474f63316873454d7578633536444b74537046684f65760a514d4e38386e426d72726862472f7a4279705a4a675279453834683066427a64385351654744786c515235376b745a696a543049564e63646a7571367654767a0a65774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
        "private_key": "2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945766749424144414e42676b71686b6947397730424151454641415343424b67776767536b41674541416f4942415144446d5a736674775931453439370a6f66754f6c5972774e3258796a4b772f584138366674474b6a6a69656d4f714d6834373151502f35483659642b325141642f637a43376c4a7a6a6a3356794b570a304a796c684951455a7870476a47784c304a436e4478487a725662484e714e314c6a377572544e4956647667586c704f455231774a754b44706c466d767a4c300a36576f6f7a44476d6d534266674d4571775141366a503561435944797061622b4c3473593032524f4b345974597932437a2b7766485257467579703056496d580a5a6e45506358376154656f6e596f344a6941743444415a4c38366270567672395a6a733568495550536f6a6f684a686359357a574777517937467a6e6f4d71310a4b6b57453536394177337a7963476175754673622f4d484b6c6b6d424849547a69485238484e33784a42345950475642486e7553316d4b4e505168553178324f0a367271394f2f4e3741674d424141454367674541454d4668786d2b354f6d61346a6443736165527069485a575a3161686b72506949684b6e4249563257432b6c0a4e2f434d30486d47382b4a414b715655526134424951424b47515a76587443364238314b2f65724348465a7771385a76714862765455412f4f323648316e7a5a0a74376f45626847734b50416836374270622f4b4c59515954745539542f6363334b442b75646c77336a4a766c61416a786779595254504b792f796439516b76440a34447441514a6857424d30313178756874324757686a6c45636e305341314459734157552f2b65426a443079347576426436386b6b495a38382b5a76552f6f340a4f47306e4154464f696d53757447672f322f54626c585644384a465667332f316562554c7454463239663337756f6d7a3153676b44596a63666b4579314939620a7934586d5448664a63466b3046707a5a59504168326b4170745a7a356e4f4336736554723736485034514b4267514433623850744a795168373952615a2f34720a567764653271374768674d79386b7a774c594e634d68394b4f504d554231797a675270387a535855435a6573556e4167412b53773256444c77704746542b43640a5645726552724f30384c56776a63536a314c6d67582b6f68346c7855377335476c334c69545a4464364755753457746e434c4b576a766c346655437237486b700a735934596b446e7569474959734b4a586c6b5745444e76346f774b426751444b5870527a3646723251562b323762717a4463396c6139624c4f61637076656a460a2b4a71487a506b6771304c3756466537366b496962586b6b375231622b5133685645643477694d6a4d6e344d5a4a7a613142526a5151594771367a7533646e720a4a394f4966794a6a35624f59575871655856434c44363372435a72426943644c377651502b6f7031437252314d4638413762534f7259557936586139385a36740a4f6a78756b64575053514b426751434443334654703167756c5172394f6e685655636b34686b37734730755562746b716c714173637573356277486d434b51690a2b5777697a712b4c4a6531724f566e69797330536b485748424b763355372b63383269585968434938726256506d2f33614a464c4336452f67746674723341560a324e33695672777a6d6f49454779533773394b4a68483142502b7a4259514d6d66722f48364a4b5637797373386c64345663444a56396f6b53774b42675143650a7431386e4b4f31756867645471552f736273426967786d4c656b516f384e46487335732f4e76754e4b38543036556d47454579655138336e7344422b6d6537510a3878433748556742717642424f416674654c676b77444c42754a4f424a473574694762586678367879733334687655736a334e4548614142337836492b7767570a2f6570645064717077534f585a6343644d6447537458547159554448364744533741484a6c6f637751514b4267444e504479684d2f5234384e76575350394e520a533052666a65336d5762564f5161306f5258567268697159454d783434526d736d546438465a30354e364c507735783263754c3950677a4a66624842556872670a756c31444d78483771303337596a443744716b67344f77702f524c54514e636c3935784749433850694c55685033427439504b674f7375735939486e736562340a366154597a58495a3376654e75736538496f6e306c3030660a2d2d2d2d2d454e442050524956415445204b45592d2d2d2d2d0a"
})):
    from hospital.api.server import advance, inspect
    from hospital.api.wallet import sym_decrypt, decrypt_msg, Decryption

    payload = {
        "did": medico.did,
        "method": "access_data",
        "data": {
            "type": "access",
            "attributes": {
                "patient_did": medico.paciente_did,
                "token": medico.token
            }
        }
    }
    result = advance(payload)

    @listen()
    def get_read_permission():
        allowed_reads = inspect("/allowed_reads")
        if medico.did in allowed_reads["response"]["allowed_reads"].get(medico.token, []):
            return medico.token
        return None
    retrieved_token = get_read_permission()
    logger.info(f"Acess granted to doctor {medico.did} for token: {retrieved_token}")

    if retrieved_token is None:
        raise HTTPException(status_code=404, detail=f"No read permission granted to doctor {medico.did} for token: {medico.token}.")
    
    data = inspect(f"/access_tokens")["response"]["access_tokens"][medico.paciente_did].get(retrieved_token)

    if data is None:
        raise HTTPException(status_code=404, detail=f"No data was shared with doctor {medico.did}.")

    decrypted_iv = decrypt_msg(Decryption(message=data["encrypted_iv"], private_key=medico.private_key))["decrypted_message"]
    decrypted_key = decrypt_msg(Decryption(message=data["encrypted_key"], private_key=medico.private_key))["decrypted_message"]
    decrypted_data = sym_decrypt(encrypted_data=data["shared_data"], key=decrypted_key, iv=decrypted_iv)

    decrypted_data = {
            "token": retrieved_token,
            "patient_did": data["patient_did"],
            "doctor_did": data["doctor_did"],
            "shared_data": decrypted_data,
            "expires_at": data["expires_at"]
    }

    payload = {
        "did": medico.did,
        "method": "remove_token",
        "data": {
            "type": "remove_token",
            "attributes": {
                "token": retrieved_token,
                "patient_did": data["patient_did"],
                "doctor_did": data["doctor_did"]
            }
        }
    }
    result = advance(payload)

    return {"response": decrypted_data, "status": "ok"}