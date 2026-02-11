import face_recognition
import pickle


def get_face_encoding(image_file):
    """
    Extract face encoding from an image.
    Only ONE face is allowed.
    """
    image=face_recognition.load_image_file(image_file)
    encoding=face_recognition.face_encodings(image)
    
    if len(encoding)==0:
        raise ValueError("No face detected")
    if len(encoding)>1:
        raise ValueError("Multiple faces detected")
    return pickle.dumps(encoding[0])

def verify_face(stored_code, image_file):
    known_code = pickle.loads(stored_code)

    image = face_recognition.load_image_file(image_file)
    encoding = face_recognition.face_encodings(image)

    if len(encoding) == 0:
        raise ValueError("No face detected")
    if len(encoding) > 1:
        raise ValueError("Multiple faces detected")

    live_code = encoding[0]

    # ✅ REAL VERIFICATION
    distance = face_recognition.face_distance(
        [known_code],
        live_code
    )[0]

    # 🔐 Threshold (VERY IMPORTANT)
    if distance < 0.5:
        return True
    return False
