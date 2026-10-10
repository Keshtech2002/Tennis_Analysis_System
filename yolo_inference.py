from ultralytics import YOLO 

model = YOLO('models/best_1280.pt')

# model.predict('input_videos/image.png', save=True)

result = model.predict('input_videos/input_video.mp4',conf=0.6, save=True)
print(result)
print("boxes:")
for box in result[0].boxes:
    print(box)