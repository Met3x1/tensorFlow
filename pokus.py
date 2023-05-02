import tensorflow as tf
import matplotlib.pyplot as plt

train_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
            "\\had\\potholeDetectionTest\\photos\\72x72 test"
test_dir = "C:\\Users\\mbali\\Desktop\\school\\kasv\\programovanie" \
           "\\had\\potholeDetectionTest\\photos\\72x72 train"

# Load the images from the directories and normalize their pixel values
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=(72, 72),
    batch_size=32
)
train_images, train_labels = next(iter(train_dataset))
train_images = train_images / 255.0

test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=(72, 72),
    batch_size=32
)
test_images, test_labels = next(iter(test_dataset))
test_images = test_images / 255.0

# Visualize the first 25 images in the training set
# plt.figure(figsize=(10,10))
# for i in range(25):
#     plt.subplot(5,5,i+1)
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i], cmap=plt.cm.binary)
# plt.show()

#setup modelu
model = tf.keras.Sequential([
    tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape=(72, 72, 3)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])


model.compile(optimizer = 'adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_images,train_labels, epochs=10)