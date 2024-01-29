from rest_framework import serializers

from users.models import User


class UserSerializers(serializers.ModelSerializer):
	fullName = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = [
			"fullName",
			"email",
			"phone",
			"avatar"
		]

		def get_fullName(self, obj):
			return f"{obj.first_name} {obj.last_name}"


class UserPasswordSerializers(UserSerializers):
	password = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ["password"]

	def get_password(self, obj):
		return obj.password1


class UserAvatarSerializers(UserSerializers):
	class Meta:
		model = User
		fields = ["avatar"]
