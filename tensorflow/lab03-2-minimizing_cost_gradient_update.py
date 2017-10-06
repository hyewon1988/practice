import tensorflow as tf

x_data = [1, 2, 3]
y_data = [1, 2, 3]

X = tf.placeholder(tf.float32)
Y = tf.placeholder(tf.float32)
W = tf.Variable(tf.random_normal([1]), name = 'weight')

# our hypothesis for linear model X * W
hypothesis = X * W

# cost/loss function
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# Minimize : Gradient descent using derivate : W -= learning rate * derivate
learning_rate = 0.1
gradient = tf.reduce_mean((W*X - Y) * X)
descent = W - learning_rate * gradient
update = W.assign(descent)

# Launch the graph in a session
sess = tf.Session()
# Initializes global variables in the graph
sess.run(tf.global_variables_initializer())

for step in range(21):
    sess.run(update, feed_dict = {X:x_data, Y: y_data})
    print(step, sess.run(cost, feed_dict = {X:x_data, Y:y_data}), sess.run(W))
