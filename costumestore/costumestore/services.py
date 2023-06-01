import cloudinary.uploader


class Cloudinary_Services:
    def store_image(image, folder, tags=[]):
        result = cloudinary.uploader.upload(
            image,
            folder=folder,
            tags=tags,
        )
        result_dict = {
            "url": result["url"],
            "public_id": result["public_id"],
        }

        return result_dict
