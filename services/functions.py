from models.models import Followers, Profile
from conections.mysql import conection_userprofile
from sqlalchemy.exc import IntegrityError

def follow_user(id_follower, id_following):
    session = conection_userprofile()

    if id_follower == id_following:
        return {"error": "You cannot follow yourself"}, 400

    # Verify actives profiles
    follower_profile = session.query(Profile).filter_by(Id_User=id_follower, Status_account=1).first()
    following_profile = session.query(Profile).filter_by(Id_User=id_following, Status_account=1).first()

    if not follower_profile or not following_profile:
        session.close()
        return {"error": "Follower or following profile not found or inactive"}, 404

    # Verify if following before
    existing = session.query(Followers).filter_by(Id_Follower=id_follower, Id_Following=id_following).first()
    if existing:
        if existing.Status == 1:
            session.close()
            return {"message": "Already following"}, 200
        else:
            existing.Status = 1
            session.commit()
            session.close()
            return {"message": "Follow re-activated"}, 200

    # Crear nueva relación
    new_follow = Followers(
        Id_Follower=id_follower,
        Id_Following=id_following,
        Status=1
    )

    try:
        session.add(new_follow)
        session.commit()
        return {"message": "Followed successfully"}, 201
    except IntegrityError:
        session.rollback()
        return {"error": "Database integrity error"}, 500
    finally:
        session.close()
