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


class HandelErrors:
    """
    A class for handling and cleaning error messages.

    Methods:
        form_errors(errors, type): Clean and return error messages based on the specified type.
    """

    def form_errors(errors, type):
        """
        Clean and return error messages based on the specified type.

        Args:
            errors (dict): A dictionary containing error messages.
            type (str): The type of output desired. Must be either 'dict' or 'list'.

        Returns:
            dict or list: Cleaned error messages based on the specified type.

        Raises:
            ValueError: If the type argument is not 'dict' or 'list'.

        """
        if type == "dict":
            clean_errors = {}
            for error in errors:
                clean_errors[error] = errors.get(error)[0]
            return clean_errors

        if type == "list":
            clean_errors = []
            for error in errors:
                clean_errors.append(errors.get(error)[0])
            return clean_errors
