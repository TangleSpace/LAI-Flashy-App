import os

import torch

import flash
from flash.core.data.utils import download_data
from flash.image import ImageClassificationData, ImageClassifier

# 1 Download data
download_data("{{ url }}", ".")

datamodule = ImageClassificationData.from_{{ method }}(
    {% for key, value in data_config.items() %}{{ key }}={% if value is string %}"{{ value }}"{% else %}{{ value }}{% endif %},{% endfor %}
    batch_size=4,
    transform_kwargs={"image_size": (196, 196), "mean": (0.485, 0.456, 0.406), "std": (0.229, 0.224, 0.225)},
)

trainer = flash.Trainer(limit_predict_batches=20)
model = ImageClassifier.load_from_checkpoint("{{ checkpoint }}")
predictions = trainer.predict(model, dataloaders=datamodule.val_dataloader(), output="fiftyone")  # output FiftyOne format

torch.save(predictions, os.path.join("{{ root }}", "{{ run_id }}_predictions.pt"))
