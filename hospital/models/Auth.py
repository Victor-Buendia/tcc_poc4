import os
import time
from hospital.models import *

class Autenticacao(BaseModel):
    public_key: str = Field(..., example="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541734e56665a535961572f596947457852347848570a6a68703164494744687a4b4b51573935504562414741467643525876794d6131365a5479584e336b707132615753506761706e6c702b676d3350706e623958310a496763423644544148424e392f3156466c4951374f47534f6b513268394d70456558303367416845422b476d2b53626657303148612f6d704b784c33546b49430a374e39625a6378684d56743463516e4a742f452f6241584c4f335142774c4132302f4d4a39707a644d6952343555514754737641704a503230644a6d6b33414d0a30327455444a31575a43754a6e4563394c592b35506456755966546b6b616172437973334c594a72702b5a5a684268615358532f592f5139745967666b6439390a3373556e433139444174554b4c4f6f6b6d57664a672f50584b7a693647737872364f38384258336c4439584747344465414c4d4d3051327663496e762f446d490a6a774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a")
    private_key: str = Field(..., example="2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945765149424144414e42676b71686b6947397730424151454641415343424b63776767536a41674541416f4942415143773156396c4a687062396949590a5446486a4564614f476e563067594f484d6f704262336b38527341594157384a46652f49787258706c504a633365536d725a705a492b42716d65576e364362630a2b6d6476316655694277486f4e4d41634533332f56555755684473345a49365244614830796b52356654654143455148346162354a743962545564722b616b720a4576644f51674c733331746c7a4745785733687843636d333854397342637337644148417344625438776e326e4e30794a486a6c52415a4f7938436b6b2f62520a306d615463417a546131514d6e565a6b4b346d63527a30746a376b3931573568394f53527071734c4b7a6374676d756e356c6d454746704a644c396a394432310a69422b52333333657853634c58304d4331516f733669535a5a386d44383963724f4c6f617a47766f377a77466665555031635962674e344173777a52446139770a69652f384f59695041674d424141454367674541542b474466326a502f587a5a65417035373035756b72446e49434d6c62467872556858754f556c6f6d792b430a6e694d58743658304a546c5170707a69486c314c33547130744e4d6969452f35786c636a684d5374514a7254784c61586c6464455571534e6b774b4d30664f790a35316d324d4b4e7966554d5159446a62716f664836734d686f4e6676444a717954612f366f5a4a32536453344c2b7338654a527565766e4638743737484774630a437244744570443073735146356d6e6562666a4345766f585a462b4e39476542632b3374386f574959394a7a41646c5233386351344b684545305567334d316a0a384a4c2b70736772507161474b7647766d4d344233464b574b6f463068796d31525a734a6f79474449452f57586c34524855694e67664c2b54644462526968490a485177775a596d667a6761536848492b54435652662f64576976374967654e6352576c303343677534514b4267514476612f65496a356a6770716e62734e505a0a414d305641394d616f566b35327646613276327771724a694e514d7a32426d727676496c31774b396e415178334c38324649776f3343375250594a75436144720a4c715256326c775452436a575a4831524c664251714c6a443038584d724236345a6b4d4838436e334664664767532b4a594767395a7578302f7573716f736a750a6e4472365168774237577a35724368326f7352703330393055514b4267514339452f52327659656e465266727255536a54353949554e444245395365444961650a6d51704b4a4e7853543455542b2b79657362506334713865316948394872567a6c455046384c38476936505a682f746a434d3337423843686f6a384b393655380a43612f77775239465342427854374571756f4b426b6b73426c6e316d2b4f4457566b376e75507730435254385776376a785447332f6965536d4f5661425048330a616d306e3666425733774b4267465857463444574f724551443457373937657447646d57375842327545364e75456f69695346316b55363051746d72654569690a784a336359426371674461414e65316c6f48706c746b4d2b45697a784e736761694d426538505058552b7a4a536b5234653966764a59375074664b54497442700a6d553658512f525a3247704b6c6f6869442f307a6b554c41776638664c587165654761516e516e7a335559462b74764e7279316c366b3642416f4741416c71740a514930376b796b41457a386c43364f434b44525a5a51344b4a36326750336c49563450392b6b686a4c3879444e6261677471396233745a7274657362393052780a5535576279306b5230544f5150627475565348546c432b672b564838444c4e534c583036466e4b2f51616e73577376587443564f4b63626c364e4a51656c71340a774d6e6332676b43366546344b76335a6b4b447066546e4b4955544f666e596b7863707a343645436759454132577355344a6b6c30625042654f5971385243380a737a48456b4d49472b63444764774e4f676647543071775274726771696f68424870387a4148636d3973626439387865477863315039743054574e6e754e44520a567333504a59697255466645526f445638746e7730374c51706c6c534942562f35456c5276346e54733673664d727545664b6569755832712f6c4a76392b41430a6a4b5a7278794238367539397a464c635149344b4665733d0a2d2d2d2d2d454e442050524956415445204b45592d2d2d2d2d0a")

    @property
    def did(self):
        return "did:key:" + hash_text_sha256(self.public_key)

def remove_auth(payload):
    did = payload["did"]
    if AppState.valid_auths.get(did):
        del AppState.valid_auths[did]
    return "accept"
@catch
def authenticate_request(payload):
    remove_auth(payload)
    did = payload["did"]

    if not any(did in x for x in [AppState.patients_list, AppState.doctors_list]):
        logger.error(f"User with DID {did} doesn't exist")
        return "reject"

    public_key = payload["data"]["public_key"]

    AppState.pending_auths[did] = {
        "challenge": os.urandom(32).hex(),
        "public_key": public_key,
        "proof": None,
    }

    return "accept"

@catch
def authenticate_response(payload):
    did = payload["did"]
    proof = payload["data"]["proof"]

    AppState.pending_auths[did]["proof"] = proof

    return "accept"

@catch
def attempt_authentication(payload):
    from hospital.api.wallet import verify_msg, Signature

    did = payload["did"]
    public_key = AppState.pending_auths[did]["public_key"]
    challenge = AppState.pending_auths[did]["challenge"]
    proof = AppState.pending_auths[did]["proof"]

    attempt = Signature(message=challenge, signature=proof, public_key=public_key)
    logger.info(f"Verifying proof for DID {did}: SIGNATURE {attempt}")

    validation = verify_msg(attempt)
    is_valid = bool(validation["is_valid"])

    logger.info(f"Proof for DID {did} is {'valid' if is_valid else 'invalid'}")

    if (is_valid):
        try:
            AppState.valid_auths[did] = {
                "status": "authenticated",
                "expires_at": time.time() + 2*60, # 2 minutes
            }
            del AppState.pending_auths[did]
        except:
            logger.error(f"Error while validating auth for DID {did}")
            return "reject"
        return "accept"
    else:
        return "reject"