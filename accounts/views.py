from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserAuth
from .serializers import UserSerializer, GoogleAuthSerializer, FacebookAuthSerializer
from django.conf import settings
from django.core.mail import send_mail
from blogs.models import Blog
from rest_framework.views import APIView



@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        full_name = request.data.get('full_name')

        if not email or not password or not full_name:
            return Response({"message": "All fields (Email, password, name) are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = UserAuth()
            user.email = email
            user.set_password(password)
            user.save()
        except Exception as e:
            return Response({"error": "The email is already taken. Please provide an unique email."}, status=status.HTTP_400_BAD_REQUEST)
        
        user.full_name = full_name
        user.save()

        # Generate OTP
        otp = user.generate_otp()


        # Send email
        try:
            send_mail(
                subject='Your Email Verification OTP',
                message = f"""
                            Hello {full_name},

                            Thank you for signing up!

                            To complete your registration, please verify your email address by entering the following 6-digit verification code:

                            {otp}

                            This code is valid for the next 5 minutes. If you did not request this verification, please ignore this email.

                            Thank you for joining us! If you have any questions, feel free to contact our support team.

                            Best regards,  
                            JVAI  
                            support@jvai.com
                            """,

                from_email= settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": "Failed to send OTP email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token


        return Response({
            'refresh': str(refresh),
            'access': str(access_token),
            'message': 'Please verify your email using the OTP sent to your email address.'
        }, status=status.HTTP_201_CREATED)




@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Both email and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if user is not None:
            user_info = UserAuth.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({
                'refresh': str(refresh),
                'access': str(access_token),
                'user_profile': UserSerializer(user_info).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        


# @api_view(['POST'])
# def verify_email(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         otp = request.data.get('otp')

#         if not email or not otp:
#             return Response({"error": "Both email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             user = UserAuth.objects.get(email=email)
#         except UserAuth.DoesNotExist:
#             return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
#         if timezone.now() > user.otp_expired:
#             return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)
        
#         elif user.otp == otp:
#             user.is_verified = True
#             user.save()
#             user = UserAuth.objects.get(email=email)
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             return Response({'status': 'success','access':access_token,"message": "Email verified successfully."}, status=status.HTTP_200_OK)
#         else:
#             return Response({'status': 'error',"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_email(request):
    if request.method == 'POST':
        otp = request.data.get('otp')

        if not otp:
            return Response({"error": "OTP are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = UserAuth.objects.get(otp=otp)
        except UserAuth.DoesNotExist:
            return Response({"error": "Invalid OTP, Please try a valid one."}, status=status.HTTP_404_NOT_FOUND)
        
        if timezone.now() > user.otp_expired:
            return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.otp == otp:
            user.is_verified = True
            user.save()
            user = UserAuth.objects.get(otp=otp)
            user.otp = None
            
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            return Response({'status': 'success','access':access_token,"message": "Email verified successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error',"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def resend_otp(request):
    email = request.data.get('email')
    user = UserAuth.objects.get(email=email)
    otp = user.generate_otp()  
    # Send email
    try:
        send_mail(
            subject='Your Email Verification OTP',
            message = f"""
                        Hello {user.full_name},

                        Thank you for signing up!

                        To complete your registration, please verify your email address by entering the following 6-digit verification code:

                        {otp}

                        This code is valid for the next 5 minutes. If you did not request this verification, please ignore this email.

                        Thank you for joining us! If you have any questions, feel free to contact our support team.

                        Best regards,  
                        JVAI  
                        support@jvai.com
                        """,

            from_email= settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({"error": "Failed to send OTP email. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response({"message": "We sent you an OTP to your email."}, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    email = request.user
    user_profile = UserAuth.objects.get(email=email)

    if request.method == 'GET':
        serializer = UserSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    data = request.data
    user = request.user
    try:
        user_profile = UserAuth.objects.get(email=user.email)
    except UserAuth.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check for restricted fields
    restricted_fields = ['email', 'is_active','is_verified', 'is_superuser', 'is_staff', 'otp']
    if any(field in data for field in restricted_fields):
        if not user.is_superuser:
            return Response({"error": "You do not have permission to change admin-related fields."},
                            status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user_profile, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Successfully Updated Profile"}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    
    if not new_password or not confirm_password:
        return Response({"error": "New password and confirm password are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    elif new_password != confirm_password:
        return Response({"error": "Password do not match."}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    user.set_password(new_password)
    user.save()
    return Response({"message": "Successfully change your password."}, status=status.HTTP_200_OK)



from donations.models import Donation
from django.db.models import Sum

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboardView(request):
    user = request.user

    if user.is_superuser:
        all_user_list = UserAuth.objects.all()
        total_stories = Blog.objects.count()
        total_donations = Donation.objects.aggregate(total=Sum('amount'))['total'] or 0
        serializer = UserSerializer(all_user_list, many=True)
        return Response({
                'all_user_list': len(all_user_list),
                'total_stories': total_stories,
                'total_donations': total_donations,
                'user_list': serializer.data
            }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Permission denied. Only admin can access this resource."},
            status=status.HTTP_403_FORBIDDEN
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def specific_user(request, pk):
    user = request.user
    if user.is_superuser:
        try:
            user_profile = UserAuth.objects.get(pk=pk)
            serializer = UserSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserAuth.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(
            {"error": "Permission denied. Only admin can access this resource."},
            status=status.HTTP_403_FORBIDDEN
        )



# @api_view(['POST'])
# def forgot_password(request):
#     email = request.data.get('email')
#     new_password = request.data.get('new_password')
#     confirm_password = request.data.get('confirm_password')

#     if new_password != confirm_password:
#         return Response({"error": "New password and confirmation password do not match."}, status=status.HTTP_400_BAD_REQUEST)

#     elif email is None or new_password is None:
#         return Response({"message": "Please provide email and new password"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = UserAuth.objects.get(email=email)
#         user.set_password(new_password)
#         user.save()
#     except:
#         return Response({"message": "Invalid Email"}, status=status.HTTP_400_BAD_REQUEST)


#     return Response({"message": "Successfully reset your password."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserAuth.objects.get(email=email)
    except UserAuth.DoesNotExist:
        return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

    otp = user.generate_otp()
    
    # Send the OTP via email
    send_mail(
        subject="Your OTP to Reset Password",
        message=f"Your OTP is: {otp}. It will expire in 5 minutes.",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({"message": "OTP sent to your email address."}, status=status.HTTP_200_OK)




# from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from rest_framework.permissions import IsAuthenticated

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def logout(request):
#     try:
#         refresh_token = request.data.get("refresh")

#         if refresh_token is None:
#             return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

#         token = RefreshToken(refresh_token)
#         token.blacklist()

#         return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
    
#     except TokenError:
#         return Response({"error": "Invalid or expired refresh token."}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error": "Something went wrong during logout."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GoogleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": True, "data": serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)





class FacebookLoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = FacebookAuthSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"success": True, "data": serializer.validated_data}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
