# TDFPS Character
# Python 2.7.14

import struct

class character:
	def __init__(self):
		self.debug = False
		self.reborn()
		self.sniperBulletNum = 5
		self.sniperBulletOwn = 30
		self.submachineBulletNum = 30
		self.submachineBulletOwn = 200
		self.prop = [0, 0, 0, 0] # 0 for nothing, 1 for +hp, 2 for barrier, 3 for +atk
		self.buffTimeLeft = [0.0, 0.0, 0.0]
		
	def reborn(self):
		self.isAlive = 1
		self.rebornTimeLeft = 0.0
		self.hp = 1000
		self.maxHp = 1000
		self.resetPosition()
		
	def resetPosition(self):
		self.position = [0.0, 3.0, 58.0]
		self.rotationY = 180.0
		
	def die(self):
		self.isAlive = 0
	
	def update(self, dt):
		self.buffTimeLeft[0] = max(0, self.buffTimeLeft[0] - dt)
		self.buffTimeLeft[1] = max(0, self.buffTimeLeft[1] - dt)
		self.buffTimeLeft[2] = max(0, self.buffTimeLeft[2] - dt)
		if self.isAlive == 0: # dead
			self.rebornTimeLeft -= dt
			if self.rebornTimeLeft <= 0:
				self.reborn()
		else: # alive
			if self.hp <= 0:
				self.die()
		if self.debug:
			self.log()
			
	def handle(self, data):
		if self.isAlive:
			self.position[0], self.position[1], self.position[2], self.rotationY = struct.unpack("=4f", data[10:26])
		self.sniperBulletNum, self.sniperBulletOwn, self.submachineBulletNum, self.submachineBulletOwn = struct.unpack("=4h", data[26:34])
		self.prop[0], self.prop[1], self.prop[2], self.prop[3] = struct.unpack("=4h", data[34:42])
	
	def serialize(self):
		return struct.pack("=hf2h4f8h3f", self.isAlive, self.rebornTimeLeft, self.hp, self.maxHp, self.position[0], self.position[1], self.position[2], self.rotationY, self.sniperBulletNum, self.sniperBulletOwn, self.submachineBulletNum, self.submachineBulletOwn, self.prop[0], self.prop[1], self.prop[2], self.prop[3], self.buffTimeLeft[0], self.buffTimeLeft[1], self.buffTimeLeft[2])
	
	def log(self):
		print [self.isAlive, self.rebornTimeLeft, self.hp], self.position, [self.sniperBulletNum, self.sniperBulletOwn], [self.submachineBulletNum, self.submachineBulletOwn], self.prop, self.buffTimeLeft
			