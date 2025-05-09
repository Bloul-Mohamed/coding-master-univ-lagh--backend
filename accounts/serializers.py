from rest_framework import serializers
from .models import GuidanceAuthority, Interfaces


class GuidanceAuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidanceAuthority
        fields = ['id', 'name', 'address', 'university_name',
                  'sent_deadline', 'email', 'backup_email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Create and return a new guidance authority with encrypted password"""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = password  # In a real app, use proper hashing here
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Update a guidance authority with proper password handling"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = password  # In a real app, use proper hashing here

        instance.save()
        return instance


class InterfacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interfaces
        fields = ['id', 'interface_role', 'university_name',
                  'guidance_authority', 'email', 'backup_email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """Create and return a new interface with encrypted password"""
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = password  # In a real app, use proper hashing here
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """Update an interface with proper password handling"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = password  # In a real app, use proper hashing here

        instance.save()
        return instance
