from rest_framework import serializers
from watchlist_app.models import Movie

class MovieSerializer(serializers.ModelSerializer):

    len_name = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        # will take all fields in model
        fields = "__all__"

        #only use few fields --> active fields will be gone from display
        # fields = ['id','name','description']

        #exclude fields
        # exclude = ['active']

    # This will add custom Serializer field --> will help in duration calculatio
    def get_len_name(self,object):
        return len(object.name)

    #field level validations
    def validate_description(self,value):
        if len(value) < 2:
            raise serializers.ValidationError("Desc is too short!")
        else:
            return value 

    #object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Descriprion should be different")
        return data       


# def name_length(value):
#     if len(value) < 2:
#             raise serializers.ValidationError("Name is too short!")
#     else:
#             return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     #Using validator
#     name = serializers.CharField(validators = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         # print(type(validated_data), type(*validated_data), type(**validated_data))
#         return Movie.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name',instance.name) 
#         instance.description = validated_data.get('description',instance.description)    
#         instance.active = validated_data.get('active',instance.active)    
#         instance.save()
#         return instance  

#     #field level validations
#     def validate_description(self,value):
#         if len(value) < 2:
#             raise serializers.ValidationError("Desc is too short!")
#         else:
#             return value 

#     #object level validation
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Descriprion should be different")
#         return data    
                          