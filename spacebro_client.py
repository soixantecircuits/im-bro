from socketIO_client import SocketIO, LoggingNamespace,SocketIONamespace, TRANSPORTS


class SpacebroClient(SocketIO):
  def __init__(
      self, host='localhost', port=None, spacebro_settings={'clientName': 'python-bro', 'channelName': 'spacebro'}, Namespace=SocketIONamespace,
      wait_for_connection=True, transports=TRANSPORTS,
      resource='socket.io', hurry_interval_in_seconds=1, **kw):
    if spacebro_settings['verbose'] == True:
      Namespace=LoggingNamespace
      import logging
      logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
      logging.basicConfig()
    self.clientName = spacebro_settings['clientName']
    self.channelName = spacebro_settings['channelName']
    super(SpacebroClient, self).__init__(
        host, port, Namespace, wait_for_connection, transports,
        resource, hurry_interval_in_seconds, **kw)
    self.on('connect', self.register)

  def register(self):
		print('spacebro connect')
		self.emit('register', {
			'clientName': self.clientName,
			'channelName': self.channelName
		})
  def emit(self, event, *args, **kw):
    if (len(args) == 1):
      args = args[0]
      args['_from'] = 'test-bro'
      args['_to'] = None
    super(SpacebroClient, self).emit(event, args, **kw)


