name = 'Лягушка'

actions = [ 'Смотреть и ждать', 'Рассказать прикол' ]

def get_actions(user):
  return actions

def enter(user, reply):
  msg = (
    'Вы заходите в дверь и видите странную человекоподобную лягушку. '
    'Она грустно смотрит в сторону петли.'
  )

  reply(msg)

def action(user, reply, text):
  if text == actions[0]:
    msg = (
      'Существо встало на табуретку, аккуратно просунуло голову в петлю, '
      'будто делая это не в первый раз, и прыгнуло с табурета. '
      'Скоро здесь начнет вонять французской кухней.'
    )

    reply(msg)
  else:
    msg = (
      'Вы рассказываете заезжаную хохму, что услышали от алхимика. '
      'Существо меняется в лице и у него появляется странная улыбка. '
      'Оно дает вам {} и засовывает вилку в розетку. Откуда здесь электричество?'
    ).format('вилку')

    reply(msg)

    user.add_item('good', 'fork')

  user.leave(reply)
