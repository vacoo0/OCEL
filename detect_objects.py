import os
import cv2
from PIL import Image
from transformers import YolosImageProcessor, YolosForObjectDetection
import torch

class ObjectDetector:
    def __init__(self, model_dir, model_type='yolos-tiny', frames_dir='./frames', video_title=None):
        self.model_dir = model_dir
        self.model_type = model_type
        self.frames_dir = frames_dir
        self.video_title = video_title
        self.model = None
        self.image_processor = None


    def initialize_model(self):
        self.model = YolosForObjectDetection.from_pretrained(self.model_dir)
        self.image_processor = YolosImageProcessor.from_pretrained(self.model_dir)

    def detect_objects(self):
        objects_detected = []

        frame_files = sorted(os.listdir(self.frames_dir))
        for frame_file in frame_files:
            if frame_file.startswith(self.video_title):
                frame_path = os.path.join(self.frames_dir, frame_file)
                print(frame_path)
                # frame = cv2.imread(frame_path)
                frame = Image.open(frame_path)

                inputs = self.image_processor(images=frame, return_tensors='pt')
                outputs = self.model(**inputs)
                # logits = outputs.logits
                # bboxes = outputs.pred_boxes
                target_sizes = torch.tensor([frame.size[::-1]])
                results = self.image_processor.post_process_object_detection(outputs, threshold=0.9,
                                                                             target_sizes=target_sizes)[0]
                for score, label, box in zip(results['scores'], results['labels'], results['boxes']):
                    box = [round(i, 2) for i in box.tolist()]
                    print(
                        f"Detected {self.model.config.id2label[label.item()]} with confidence "
                        f"{round(score.item(), 3)} at location {box}"
                    )
                objects_detected.append([self.model.config.id2label[label.item()] for label in results['labels']])
        return objects_detected
