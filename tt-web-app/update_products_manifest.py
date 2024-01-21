#!/usr/bin/env python
import json
import os


def update_products_manifest():
    """
    This function updates the products manifest file with the latest product urls.
    """

    def get_weights(data):
        weights = []
        for spec in data["specs"]:
            if "weight" in spec["key"].lower():
                weights.append(spec)
        return weights

    manifest = []
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    mec_dir = os.path.join(curr_dir, "../products/data/mec")
    for filename in os.listdir(mec_dir):
        filepath = os.path.join(mec_dir, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath) as f:
            data = f.read()
            data = json.loads(data)
            manifest.append({
              "title": data["name"],
              "description": data["description"],
              "image": data["img_hrefs"][0],
              "weights": get_weights(data),
            })

    with open(os.path.join(curr_dir, "./src/components/views/products_manifest.json"), "w") as f:
        f.write(json.dumps(manifest, indent=2, sort_keys=True))


update_products_manifest()
