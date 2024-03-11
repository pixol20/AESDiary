import os.path
import pickle
import encryptor
FilePath = 'save'


def SaveFile(Entries, Password):
    with open(FilePath, 'wb') as file:
        SerializedDiary = pickle.dumps(Entries)
        pickle.dump(encryptor.EncryptDiary(SerializedDiary, Password), file)




def LoadFile(password):
    if CheckFile():
        with open(FilePath, 'rb') as file:
            EncyptedEncryptedEntries = pickle.load(file)
            return pickle.loads(encryptor.DecryptDiary(EncyptedEncryptedEntries, password))


def CheckFile():
    return os.path.exists(FilePath)