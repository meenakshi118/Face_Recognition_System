import os
import sys
import cv2
import torch
import numpy as np
import pickle
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
from tqdm import tqdm
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Load MTCNN for face detection
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
mtcnn = MTCNN(image_size=160, margin=20, min_face_size=40, device=device)

# Load FaceNet model
model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Path to dataset folder
dataset_path = "dataset"

# Optional: accept a student_id to filter
student_id = sys.argv[1] if len(sys.argv) > 1 else None

# Storage lists
embedding_list = []
name_list = []

# Load existing embeddings if available
if os.path.exists('face_embeddings.pkl'):
    with open('face_embeddings.pkl', 'rb') as f:
        data = pickle.load(f)
    embedding_list = list(data.get('embeddings', []))
    name_list = list(data.get('names', []))

# If a student_id is provided, remove their previous embeddings
if student_id:
    print(f"🔄 Re-training embeddings for Student ID: {student_id}")
    filtered_embeddings = []
    filtered_names = []
    
    for emb, name in zip(embedding_list, name_list):
        if name != student_id:
            filtered_embeddings.append(emb)
            filtered_names.append(name)
    
    embedding_list = filtered_embeddings
    name_list = filtered_names
    person_dirs = [student_id]
else:
    print("⚡ Generating embeddings for all students...")
    person_dirs = os.listdir(dataset_path)

# Loop through dataset directory
for person_name in person_dirs:
    person_folder = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_folder):
        continue

    print(f"Processing: {person_name}")

    for image_name in tqdm(os.listdir(person_folder)):
        image_path = os.path.join(person_folder, image_name)

        try:
            img = Image.open(image_path).convert('RGB')
            face = mtcnn(img)
            if face is not None:
                face_embedding = model(face.unsqueeze(0).to(device)).detach().cpu().numpy()
                embedding_list.append(face_embedding[0])
                name_list.append(person_name)
        except Exception as e:
            print(f"Failed on {image_path}: {e}")

# Convert to numpy arrays
embedding_array = np.array(embedding_list)
name_array = np.array(name_list)

# Save embeddings and names to pickle
data = {
    "embeddings": embedding_array,
    "names": name_array
}
with open("face_embeddings.pkl", "wb") as f:
    pickle.dump(data, f)

if student_id:
    print(f"✅ Embeddings for Student ID: {student_id} updated successfully!")
else:
    print("✅ Face embeddings for all students generated and saved to face_embeddings.pkl")