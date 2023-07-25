"""Updates User abilities in firestore"""
import fireo

from common.models import UserAbility, LearningUnit, User

def update_user_abilites(user_ability, learning_unit_id):
  """Updates User ability for a particular learning unit"""
  print("Updating User Abilitites")
  learning_unit = LearningUnit.find_by_id(learning_unit_id)
  if learning_unit:
    batch = fireo.batch()
    count = 0
    for user_id, ability in user_ability.items():
      user = User.find_by_id(user_id)
      if count >450:
        batch.commit()
        count = 0
      count += 1
      if user:
        ability_item = UserAbility.collection.filter(
          user=user.key).filter(learning_unit=learning_unit.key).get()
        if ability_item:
          ability_item.ability = float(ability)
          ability_item.learning_unit = learning_unit
          ability_item.user = user
          ability_item.update(batch=batch)
        else:
          ability_item = UserAbility()
          ability_item.user = user
          ability_item.learning_unit = learning_unit
          ability_item.ability = float(ability)
          ability_item.save(batch=batch)
    batch.commit()
