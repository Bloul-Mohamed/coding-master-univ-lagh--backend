# Fix for projects/serializers.py
from rest_framework import serializers
from .models import Project, Student
from accounts.models import GuidanceAuthority


class StudentSerializer(serializers.ModelSerializer):
    # Explicitly define id field to make it visible in Swagger
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number',
                  'university_name', 'country', 'project', 'field_of_study', 'branch',
                  'user_id', 'uuid', 'id_individual', 'establishment_id', 'user_name']


class ProjectSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'send_date', 'update_date',
                  'status', 'guidance_authority', 'deadline', 'email',
                  'backup_email', 'password', 'students', 'is_complete']  # Added password
        extra_kwargs = {
            'password': {'write_only': True},
            'send_date': {'read_only': True},
            'update_date': {'read_only': True},
        }

    def create(self, validated_data):
        students_data = validated_data.pop('students', [])
        password = validated_data.pop('password', None)

        project = Project(**validated_data)
        if password:
            project.password = password  # In a real app, use proper hashing here
        project.save()

        for student_data in students_data:
            Student.objects.create(project=project, **student_data)

        return project

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        students_data = validated_data.pop('students', [])

        # Update the project instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.password = password  # In a real app, use proper hashing here

        instance.save()

        # Handle students if provided
        if students_data:
            instance.students.all().delete()  # Remove existing students
            for student_data in students_data:
                Student.objects.create(project=instance, **student_data)

        return instance


class ProjectStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('S', 'sent'),
        ('P', 'In progress'),
        ('CDE', 'Directed to CDE'),
        ('CATI', 'Directed to CATI'),
        ('bi', 'Directed to Business Incubator'),
        ('I', 'Inadmissible'),
        ('N', 'None'),
    ])
