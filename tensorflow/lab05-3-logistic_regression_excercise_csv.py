import tensorflow as tf

fliename_queue = tf.train.string_input_producer(["data-03-diabetes.csv"],  shuffle = False, name = "filename_queue")

reader = tf.TextLineReader()
key, value = reader.read(fliename_queue)

# Default values, in case of empty columns, Also specifies the type of the decoded default
record_deafults = [[0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.], [0.]]
xy = tf.decode_csv(value, record_defaults = record_deafults)

# collect batches of csv in
train_x_batch, train_y_batch = tf.train.batch([xy[0:-1], xy[-1:]], batch_size = 10)

# placeholders for a tensor that will be always fed
X = tf.placeholder(tf.float32, shape = [None, 8])
Y = tf.placeholder(tf.float32, shape = [None, 1])

W = tf.Variable(tf.random_normal([8, 1]), name = "weight")
b = tf.Variable(tf.random_normal([1]), name = "bias")

# Hypothesis using sigmoid
hypothesis = tf.sigmoid(tf.matmul(X, W) + b)

# cost/loss function
cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1-Y) * tf.log(1-hypothesis))

train = tf.train.GradientDescentOptimizer(learning_rate = 0.01).minimize(cost)

# Accuracy computation
# True if hypothesis > 0.5 else False
predicted = tf.cast(hypothesis > 0.5, dtype = tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), dtype=tf.float32))

# Launch graph
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    # Start populating the filename queue
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    for step in range(100001):
        x_batch, y_batch = sess.run([train_x_batch, train_y_batch])
        cost_val, _ = sess.run([cost, train], feed_dict = {X: x_batch, Y: y_batch})
        if step % 200 == 0:
            print(step, cost_val)
    # Accuracy report
    h, c, a = sess.run([hypothesis, cost, accuracy], feed_dict = {X:x_batch, Y: y_batch})
    print("\nHypothesis: ", h, "\nCorrect (Y): ", c, "\nAccuracy: ", a)

    coord.request_stop()
    coord.join(threads)
