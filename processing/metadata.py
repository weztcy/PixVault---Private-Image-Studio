from PIL import Image


class MetadataProcessor:
    def process(self, image, settings):

        mode = settings.get("mode", "all")

        return self.remove_metadata(image, mode, settings)

    def remove_metadata(self, image, mode, settings):

        if mode == "preserve":
            return image.copy()

        clean = image.copy()

        if mode == "all":
            return self.clear_all(clean)

        if mode == "custom":
            return self.remove_custom(clean, settings.get("remove", []))

        raise ValueError(f"Unsupported metadata mode: {mode}")

    def clear_all(self, image):

        image.info.clear()

        if "exif" in image.info:
            del image.info["exif"]

        return image

    def remove_custom(self, image, remove_list):

        remove_list = [item.lower() for item in remove_list]

        # EXIF

        if "exif" in remove_list:
            image.info.pop("exif", None)

        # ICC PROFILE

        if "icc_profile" in remove_list:
            image.info.pop("icc_profile", None)

        # XMP

        if "xmp" in remove_list:
            image.info.pop("xmp", None)

        # IPTC

        if "iptc" in remove_list:
            image.info.pop("iptc", None)

        # SOFTWARE

        if "software" in remove_list:
            image.info.pop("software", None)

        # COPYRIGHT

        if "copyright" in remove_list:
            image.info.pop("copyright", None)

        # GPS

        if "gps" in remove_list:
            self.remove_gps(image)

        # MAKER NOTES

        if "maker_notes" in remove_list:
            self.remove_maker_notes(image)

        return image

    def remove_gps(self, image):

        exif = image.getexif()

        if not exif:
            return

        gps_tag = 34853

        if gps_tag in exif:
            del exif[gps_tag]

        image.info["exif"] = exif.tobytes()

    def remove_maker_notes(self, image):

        exif = image.getexif()

        if not exif:
            return

        maker_note_tag = 37500

        if maker_note_tag in exif:
            del exif[maker_note_tag]

        image.info["exif"] = exif.tobytes()

    def get_metadata(self, image_path):

        with Image.open(image_path) as image:
            return {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "info": dict(image.info),
                "exif": dict(image.getexif()),
            }
