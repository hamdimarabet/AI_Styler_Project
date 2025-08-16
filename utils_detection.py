import cv2
import mediapipe as mp

mp_face = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

def analyze_body_and_face(image_path, debug=False):
    """
    Analyze the body and face of a person from an image and return:
    - morphotype: Inverted Triangle, Pear, Rectangle, Hourglass
    - head_shape: Round, Long, Oval
    """
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    morphotype = "Unknown"
    head_shape = "Unknown"

    # --- Pose detection ---
    with mp_pose.Pose(static_image_mode=True) as pose:
        results_pose = pose.process(image_rgb)

    if results_pose.pose_landmarks:
        landmarks = results_pose.pose_landmarks.landmark

        # Extract key landmarks
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        left_waist = landmarks[25]
        right_waist = landmarks[26]

        # Normalized distances
        shoulder_width = abs(left_shoulder.x - right_shoulder.x)
        hip_width = abs(left_hip.x - right_hip.x)
        waist_width = abs(left_waist.x - right_waist.x)

        # Ratios
        shoulder_to_hip = shoulder_width / hip_width
        shoulder_to_waist = shoulder_width / waist_width
        hip_to_waist = hip_width / waist_width

        if debug:
            print(f"DEBUG ratios: shoulder/hip={shoulder_to_hip:.2f}, shoulder/waist={shoulder_to_waist:.2f}, hip/waist={hip_to_waist:.2f}")

        # Updated thresholds for better accuracy
        if shoulder_to_hip > 1.2 and shoulder_to_waist > 1.15:
            morphotype = "Inverted Triangle"
        elif hip_to_waist > 1.15:
            morphotype = "Pear"
        elif 0.9 <= shoulder_to_hip <= 1.1:
            morphotype = "Rectangle"
        else:
            morphotype = "Hourglass"

    # --- Face detection ---
    with mp_face.FaceMesh(static_image_mode=True) as face_mesh:
        results_face = face_mesh.process(image_rgb)

    if results_face.multi_face_landmarks:
        face_points = results_face.multi_face_landmarks[0].landmark
        xs = [p.x for p in face_points]
        ys = [p.y for p in face_points]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        ratio = width / height

        if debug:
            print(f"DEBUG face width={width:.2f}, height={height:.2f}, ratio={ratio:.2f}")

        if ratio > 0.88:
            head_shape = "Round"
        elif ratio < 0.78:
            head_shape = "Long"
        else:
            head_shape = "Oval"

    return {
        "morphotype": morphotype,
        "head_shape": head_shape
    }

# Example test
if __name__ == "__main__":
    result = analyze_body_and_face("test_image.jpg", debug=True)
    print("Detected:", result)
