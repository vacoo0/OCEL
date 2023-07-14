import os
from PIL import Image
from transformers import YolosImageProcessor, YolosForObjectDetection
import torch

class ObjectDetector:
    """
    A Class for detecting the objects in the frames using yolos-tiny.
    """
    def __init__(self, model_dir, frames_dir='./frames', video_title=None):
        """
        :param string model_dir:   location of the model
        :param string frames_dir:  directory with the extracted frames
        :param string video_title: title of the video
        """
        self.model_dir = model_dir
        self.frames_dir = frames_dir
        self.video_title = video_title.rsplit('.', 1)[0]  # remove file extension, if any
        self.model = None
        self.image_processor = None


    def initialize_model(self):
        self.model = YolosForObjectDetection.from_pretrained(self.model_dir)
        self.image_processor = YolosImageProcessor.from_pretrained(self.model_dir)

    def detect_objects(self):
        """
        Detects objects in each frame. Iterates over each frame with the matching video title in the frame directory.
        Returns a list of lists of detected objects.
        """
        objects_detected = []

        frame_files = sorted(os.listdir(self.frames_dir))
        for frame_file in frame_files:
            if frame_file.startswith(self.video_title):
                frame_path = os.path.join(self.frames_dir, frame_file)
                print(frame_path)
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
