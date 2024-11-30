import os
import base64 

from typing import Union, List
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, APIRouter

encryption = APIRouter(
    prefix="/rsa",
    tags=["Wallet"],
)

class Signature(BaseModel):
    message: str = Field(..., example="Sign me, please!")
    signature: str = Field(..., example="58aa9a762a835c962e0d9bea995b20735bbeee09f36be967b5941fbf01257b49c33a3a35aabd8cdd8400685f77c147e6f913233c06cb8c8fa9a9ab060ee761daa3bc623573f2657452b3d6fb21f3d5f1669e95a36fcef5265a18a8447c096454df107e9ff50b300fb7e368f50e822b2b7f2c9aa44016d0a958b94bcf7825a52d533f9e2903e56a0ad3e2703da247aed23216a640d89368fe9b38c9adafcf889981bbfd6e39e7a5c3f2df7290a38ae22e5fc1360e69df06ceb8662cb0c123e601873f7ce4f5e128b21caeb01aa6da247d4db82c2fb8584e847d48184877973dbcac99008137da1365058e0f728ec244c771e487c44f00b874549a212de88dc57a")
    public_key: str = Field(..., example="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541734e56665a535961572f596947457852347848570a6a68703164494744687a4b4b51573935504562414741467643525876794d6131365a5479584e336b707132615753506761706e6c702b676d3350706e623958310a496763423644544148424e392f3156466c4951374f47534f6b513268394d70456558303367416845422b476d2b53626657303148612f6d704b784c33546b49430a374e39625a6378684d56743463516e4a742f452f6241584c4f335142774c4132302f4d4a39707a644d6952343555514754737641704a503230644a6d6b33414d0a30327455444a31575a43754a6e4563394c592b35506456755966546b6b616172437973334c594a72702b5a5a684268615358532f592f5139745967666b6439390a3373556e433139444174554b4c4f6f6b6d57664a672f50584b7a693647737872364f38384258336c4439584747344465414c4d4d3051327663496e762f446d490a6a774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a")

class Encryption(BaseModel):
    message: str = Field(..., example="Encrypt me, please!")
    public_key: str = Field(..., example="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b434151454130454f62426b703476334c6765416f75586d57500a4332656d58452b644d2f66584463656b4845566a70615a724f77744441326f724e3176765447634d4e49465837523339722b4b3475504d76594c56704a4361560a7337576f4b63727a586d32675a494b4e66537443562b4a416d463671715262465268586f326b6375306d57575877562b503553342f4f7871704172505457476f0a52432f57463062374d74563264586958586870762b48585367552f6a316e3157715a4f455161697a7466477573427679426f355946546b714e595344797169480a66524f704d32786d775a704748556e7156464c4563484b57776b6431646d6f392f5757386146486172446c756e6778352f4a57582b527939584d4171637553580a4a553974523273664870456b536c6c4972497237486d6347686549356c796f307869536f74625073796147466c66753336356d636846466e723663436449636e0a4b514944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a")


class Decryption(BaseModel):
    message: str = Field(..., example="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b4341514541734e56665a535961572f596947457852347848570a6a68703164494744687a4b4b51573935504562414741467643525876794d6131365a5479584e336b707132615753506761706e6c702b676d3350706e623958310a496763423644544148424e392f3156466c4951374f47534f6b513268394d70456558303367416845422b476d2b53626657303148612f6d704b784c33546b49430a374e39625a6378684d56743463516e4a742f452f6241584c4f335142774c4132302f4d4a39707a644d6952343555514754737641704a503230644a6d6b33414d0a30327455444a31575a43754a6e4563394c592b35506456755966546b6b616172437973334c594a72702b5a5a684268615358532f592f5139745967666b6439390a3373556e433139444174554b4c4f6f6b6d57664a672f50584b7a693647737872364f38384258336c4439584747344465414c4d4d3051327663496e762f446d490a6a774944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a")
    private_key: Union[str, List[str]] = Field(..., example="2d2d2d2d2d424547494e2050524956415445204b45592d2d2d2d2d0a4d494945765149424144414e42676b71686b6947397730424151454641415343424b63776767536a41674541416f4942415143773156396c4a687062396949590a5446486a4564614f476e563067594f484d6f704262336b38527341594157384a46652f49787258706c504a633365536d725a705a492b42716d65576e364362630a2b6d6476316655694277486f4e4d41634533332f56555755684473345a49365244614830796b52356654654143455148346162354a743962545564722b616b720a4576644f51674c733331746c7a4745785733687843636d333854397342637337644148417344625438776e326e4e30794a486a6c52415a4f7938436b6b2f62520a306d615463417a546131514d6e565a6b4b346d63527a30746a376b3931573568394f53527071734c4b7a6374676d756e356c6d454746704a644c396a394432310a69422b52333333657853634c58304d4331516f733669535a5a386d44383963724f4c6f617a47766f377a77466665555031635962674e344173777a52446139770a69652f384f59695041674d424141454367674541542b474466326a502f587a5a65417035373035756b72446e49434d6c62467872556858754f556c6f6d792b430a6e694d58743658304a546c5170707a69486c314c33547130744e4d6969452f35786c636a684d5374514a7254784c61586c6464455571534e6b774b4d30664f790a35316d324d4b4e7966554d5159446a62716f664836734d686f4e6676444a717954612f366f5a4a32536453344c2b7338654a527565766e4638743737484774630a437244744570443073735146356d6e6562666a4345766f585a462b4e39476542632b3374386f574959394a7a41646c5233386351344b684545305567334d316a0a384a4c2b70736772507161474b7647766d4d344233464b574b6f463068796d31525a734a6f79474449452f57586c34524855694e67664c2b54644462526968490a485177775a596d667a6761536848492b54435652662f64576976374967654e6352576c303343677534514b4267514476612f65496a356a6770716e62734e505a0a414d305641394d616f566b35327646613276327771724a694e514d7a32426d727676496c31774b396e415178334c38324649776f3343375250594a75436144720a4c715256326c775452436a575a4831524c664251714c6a443038584d724236345a6b4d4838436e334664664767532b4a594767395a7578302f7573716f736a750a6e4472365168774237577a35724368326f7352703330393055514b4267514339452f52327659656e465266727255536a54353949554e444245395365444961650a6d51704b4a4e7853543455542b2b79657362506334713865316948394872567a6c455046384c38476936505a682f746a434d3337423843686f6a384b393655380a43612f77775239465342427854374571756f4b426b6b73426c6e316d2b4f4457566b376e75507730435254385776376a785447332f6965536d4f5661425048330a616d306e3666425733774b4267465857463444574f724551443457373937657447646d57375842327545364e75456f69695346316b55363051746d72654569690a784a336359426371674461414e65316c6f48706c746b4d2b45697a784e736761694d426538505058552b7a4a536b5234653966764a59375074664b54497442700a6d553658512f525a3247704b6c6f6869442f307a6b554c41776638664c587165654761516e516e7a335559462b74764e7279316c366b3642416f4741416c71740a514930376b796b41457a386c43364f434b44525a5a51344b4a36326750336c49563450392b6b686a4c3879444e6261677471396233745a7274657362393052780a5535576279306b5230544f5150627475565348546c432b672b564838444c4e534c583036466e4b2f51616e73577376587443564f4b63626c364e4a51656c71340a774d6e6332676b43366546344b76335a6b4b447066546e4b4955544f666e596b7863707a343645436759454132577355344a6b6c30625042654f5971385243380a737a48456b4d49472b63444764774e4f676647543071775274726771696f68424870387a4148636d3973626439387865477863315039743054574e6e754e44520a567333504a59697255466645526f445638746e7730374c51706c6c534942562f35456c5276346e54733673664d727545664b6569755832712f6c4a76392b41430a6a4b5a7278794238367539397a464c635149344b4665733d0a2d2d2d2d2d454e442050524956415445204b45592d2d2d2d2d0a")


@encryption.get("/")
def root():
    return {"Health Status": "OK"}

@encryption.post("/sym_encrypt")
def sym_encrypt(data: str, key: str):
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = sym_padding.PKCS7(128).padder()
    
    padded_data = padder.update(data.encode()) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return {
        "iv": base64.b64encode(iv).decode(),
        "encrypted_message": base64.b64encode(encrypted_data).decode()
    }

@encryption.post("/sym_decrypt")
def sym_decrypt(encrypted_data: str, key: str, iv: str):
    iv = base64.b64decode(iv)
    encrypted_data = base64.b64decode(encrypted_data)
    
    cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    unpadder = sym_padding.PKCS7(128).unpadder()
    
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    
    return decrypted_data.decode()

@encryption.get("/keygen")
def rsa_keygen():
    c = Cryptography()
    c.generate_keys()
    return {
        "public_key": c.keys.get("public_key"),
        "private_key": c.keys.get("private_key"),
    }

@encryption.post("/encrypt")
def encrypt_msg(encrypt: Encryption):
    c = Cryptography()
    try:
        return {
            "message": encrypt.message,
            "encrypted_message": c.encrypt(encrypt.message, encrypt.public_key),
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Check if message has 180 characters or less."
        }

@encryption.post("/decrypt")
def decrypt_msg(decrypt: Decryption):
    c = Cryptography()
    try:
        pvk = c.retrieve_pvk(decrypt.private_key)
        return {
            "encrypted_message": decrypt.message,
            "decrypted_message": c.decrypt(decrypt.message, pvk),
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Check if private key is correct."
        }

@encryption.post("/sign")
def sign_msg(sign: Decryption):
    c = Cryptography()
    try:
        signature = c.sign(sign.message, sign.private_key)
        return {
            "message": sign.message,
            "signature": signature,
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Check if message, private key have the correct format."
        }


@encryption.post("/verify")
def verify_msg(verify: Signature):
    c = Cryptography()
    try:
        is_valid = c.verify_signature(verify.message, verify.signature, verify.public_key)
        return {
            "message": verify.message,
            "signature": verify.signature,
            "is_valid": is_valid,
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Check if message, signature, public key have the correct format."
        }


class Cryptography:
    def __init__(self):
        self.__private_key = None
        self.__public_key = None

    def generate_keys(self):
        self.__private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        self.__public_key = self.__private_key.public_key()

    def load_keys(self, public_key: hex, private_key: hex):
        self.__private_key = serialization.load_pem_private_key(
            bytes.fromhex(private_key), password=None, backend=default_backend()
        )
        self.__public_key = serialization.load_pem_public_key(
            bytes.fromhex(public_key), backend=default_backend()
        )

    @property
    def keys(self):
        return {
            "private_key": (
                self.__private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                ).hex()
            ),
            "public_key": (
                self.__public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                ).hex()
            ),
        }

    def sign(self, message, private_key=None):
        if private_key:
            key_to_verify = serialization.load_pem_private_key(
                bytes.fromhex(private_key), password=None, backend=default_backend()
            )
        else:
            key_to_verify = self.__private_key
        signature = key_to_verify.sign(
            message.encode(), padding.PKCS1v15(), hashes.SHA256()
        )
        return signature.hex()

    def verify_signature(self, message, signature, public_key=None):
        if public_key:
            key_to_verify = serialization.load_pem_public_key(
                bytes.fromhex(public_key), backend=default_backend()
            )
        else:
            key_to_verify = self.__public_key
        try:
            key_to_verify.verify(
                bytes.fromhex(signature),
                message.encode(),
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True
        except Exception:
            return False

    def encrypt(self, message, public_key=None):
        if public_key:
            key_to_verify = serialization.load_pem_public_key(
                bytes.fromhex(public_key), backend=default_backend()
            )
        else:
            print("No public_key")
            key_to_verify = self.__public_key
        encrypted_message = key_to_verify.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return encrypted_message.hex()

    def decrypt(self, encrypted_message, private_key=None):
        if private_key:
            key_to_verify = serialization.load_pem_private_key(
                bytes.fromhex(private_key), password=None, backend=default_backend()
            )
        else:
            key_to_verify = self.__private_key
        decrypted_message = key_to_verify.decrypt(
            bytes.fromhex(encrypted_message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return decrypted_message.decode()

    def retrieve_pvk(self, pvk_chunks):
        if isinstance(pvk_chunks, List):
            pvk = "".join(
                [self.decrypt(pvk_chunk, backend_pvt_k) for pvk_chunk in pvk_chunks]
            )
        else:
            pvk = pvk_chunks
        return pvk
