import cloudinary.uploader


class CloudinaryServices:
    """
    Handles Cloudinary image upload and deletion services.
    """

    def store_image(image, folder, tags=""):
        """
        Uploads an image to Cloudinary and returns the URL and public ID of the stored image.

        Args:
            image (str): The path or URL of the image file to be uploaded.
            folder (str): The folder name in Cloudinary where the image should be stored.
            tags (list, optional): A list of tags to assign to the uploaded image. Default is an empty list.

        Returns:
            dict: A dictionary containing the URL and public ID of the stored image.

        Raises:
            cloudinary.exceptions.Error: If there is an error during the image upload process.
        """
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

    def delete_image(image_id):
        """
        Deletes an image from Cloudinary.

        Args:
            image (str): The public ID of the image to delete.

        Raises:
            cloudinary.exceptions.Error: If an error occurs during the deletion process.
        """
        cloudinary.uploader.destroy(image_id)
