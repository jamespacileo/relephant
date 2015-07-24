

app = angular.module "DragonDemoApp", [
    'SwampDragonServices',
]

app.controller "GameCommentsCtrl", ($scope, $dragon)->

    $scope.todoList = {}
    $scope.todoItems = []
    $scope.channel = 'global'

    $scope.comments = []

    $scope.commentForm = {
        text: ""
        command: null
    }

    # RPGJS.Materials = {
    #     "characters": {
    #         "1": "chara.png"
    #     }
    # }



    RPGJS.defines({
        canvas: "game-canvas"
        # autoload: false
    }).ready ()->
        RPGJS.Scene.map();

        # RPGJS.Player.moveto(10, 6)
        # RPGJS.Player.moveRoute(["bottom", "speed_3"])

    $("body").on "keydown", "textarea", (event)->
      event.stopPropagation()
      console.log "KEYDOWN!"

    $scope.$watch "commentForm.text", (newVal)->
      if not newVal
        $scope.commentForm.command = null
        return

      if newVal.toLowerCase().indexOf("up") >= 0
        $scope.commentForm.command = "up"
        return

      if newVal.toLowerCase().indexOf("down") >= 0
        $scope.commentForm.command = "down"
        return

      if newVal.toLowerCase().indexOf("left") >= 0
        $scope.commentForm.command = "left"
        return

      if newVal.toLowerCase().indexOf("right") >= 0
        $scope.commentForm.command = "right"
        return

      $scope.commentForm.command = null

    swampdragon.ready ()->
      console.log "ready"
      # swampdragon.subscribe 'game-comment', $scope.channel, null, (context, data) ->
      #   console.log "subscribe", context, data
      #   @dataMapper = new DataMapper(data)
      #   return

      swampdragon.subscribe 'game', $scope.channel, null, (context, data) ->
        console.log "subscribe", context, data
        @dataMapper = new DataMapper(data)
        return

      swampdragon.onChannelMessage (channels, message) ->
        console.log "onChannelMessage", channels, message
        if message.data.type == "comment"
          $scope.comments.push message.data
          $scope.$apply()
        if message.data.type == "move"
          new_pos = message.data.position
          if message.data.direction == "bottom"
            new_pos[1] -= 1
          if message.data.direction == "top"
            new_pos[1] += 1
          if message.data.direction == "left"
            new_pos[0] += 1
          if message.data.direction == "right"
            new_pos[0] -= 1

          RPGJS.Player.moveto(new_pos[0], new_pos[1])
          RPGJS.Player.moveRoute([message.data.direction, "speed_3"])

        for i of channels
          if channels[i] == 'game-comment'
            @news = @dataMapper.mapData(@news, message.data)
        return



      # swampdragon.onChannelMessage (channels, message) ->
      #   console.log "onChannelMessage", channels, message
      #   $scope.comments.push message.data
      #   $scope.$apply()

    # $dragon.onReady ->
    #   $dragon.subscribe('game-comment', $scope.channel, todo_list__id: 1).then (response) ->
    #     $scope.dataMapper = new DataMapper(response.data)
    #     return
    #   # $dragon.getSingle('todo-list', id: 1).then (response) ->
    #   #   $scope.todoList = response.data
    #   #   return
    #   $dragon.getList('game-comment', list_id: 1).then (response) ->
    #     $scope.gameComments = response.data
    #     return
    #   return

    # $dragon.onChannelMessage (channels, message) ->
    #   if indexOf.call(channels, $scope.channel) > -1
    #     $scope.$apply ->
    #       $scope.dataMapper.mapData $scope.todoItems, message
    #       return
    #   return

    # $scope.gameCommentDone = (item) ->
    #   item.done = true != item.done
    #   $dragon.update 'game-comment', item
    #   return



    $scope.commentCreate = ($event)->
        $event.preventDefault()

        # $dragon.create('game-comment', {
        #     text: $scope.commentForm.text
        #     # ip_address: "127.0.0.1"

        # }).then (response)->
        #     console.log(response.data)

        # swampdragon.create 'game-comment', {
        #     comment: $scope.commentForm.text
        #     command: $scope.commentForm.command
        # },
        # (context, data)->
        #   console.log context, data
        # ,
        # (context, data)->
        #   console.log context, data


        swampdragon.callRouter 'send_command', 'game', {
            comment: $scope.commentForm.text
            command: $scope.commentForm.command
        },
        (context, data)->
          console.log context, data
        ,
        (context, data)->
          console.log context, data


    return