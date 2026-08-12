"""
AgriVision AI - Model Training Script
Train CNN model for plant disease detection
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os


def create_model(input_shape=(224, 224, 3), num_classes=2):
    """
    Create CNN model for plant disease detection.

    Architecture:
    - 3 Convolutional blocks
    - 3 Dense layers
    - Softmax output
    """
    model = models.Sequential([
        # Convolutional Block 1
        layers.Conv2D(32, (3, 3), activation='relu', padding='same',
                      input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Convolutional Block 2
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Convolutional Block 3
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),

        # Flatten and Dense Layers
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),

        # Output Layer
        layers.Dense(num_classes, activation='softmax')
    ])

    return model


def prepare_data(data_dir, img_size=(224, 224), batch_size=4):
    """
    Prepare data generators with augmentation.
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1.0/255,
        rotation_range=30,
        width_shift_range=0.3,
        height_shift_range=0.3,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.2,
        brightness_range=[0.7, 1.3],
        fill_mode='nearest',
        validation_split=0.2
    )

    # Only rescaling for validation
    val_datagen = ImageDataGenerator(
        rescale=1.0/255,
        validation_split=0.2
    )

    # Load training data
    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    # Load validation data
    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    return train_generator, val_generator


def train_model(data_dir, epochs=100, batch_size=4):
    """
    Train the CNN model.
    """
    print("=" * 60)
    print("AgriVision AI - Model Training")
    print("=" * 60)

    # Check if data directory exists
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' not found!")
        print("Please organize your images in the following structure:")
        print(f"  {data_dir}/")
        print(f"    healthy_leaves/")
        print(f"      img1.jpg")
        print(f"      img2.jpg")
        print(f"    diseased_leaves/")
        print(f"      img1.jpg")
        print(f"      img2.jpg")
        return None

    # Check image counts
    healthy_dir = os.path.join(data_dir, 'healthy_leaves')
    diseased_dir = os.path.join(data_dir, 'diseased_leaves')

    if os.path.exists(healthy_dir) and os.path.exists(diseased_dir):
        healthy_count = len([f for f in os.listdir(healthy_dir)
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
        diseased_count = len([f for f in os.listdir(diseased_dir)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

        print(f"\nDataset Statistics:")
        print(f"  Healthy leaves: {healthy_count} images")
        print(f"  Diseased leaves: {diseased_count} images")
        print(f"  Total: {healthy_count + diseased_count} images")
    else:
        print("Warning: Image directories not found. Proceeding anyway...")

    # Prepare data
    print("\nPreparing data generators...")
    train_gen, val_gen = prepare_data(data_dir, batch_size=batch_size)

    # Create model
    print("\nCreating CNN model...")
    model = create_model()
    model.summary()

    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=5,
            min_lr=1e-7
        )
    ]

    # Train model
    print("\nStarting training...")
    history = model.fit(
        train_gen,
        epochs=epochs,
        validation_data=val_gen,
        callbacks=callbacks
    )

    # Evaluate model
    print("\nEvaluating model...")
    val_loss, val_acc = model.evaluate(val_gen)
    print(f"\nFinal Validation Accuracy: {val_acc*100:.2f}%")
    print(f"Final Validation Loss: {val_loss:.4f}")

    return model, history


def save_model(model, model_dir='model'):
    """
    Save trained model.
    """
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = os.path.join(model_dir, 'plant_disease_model.h5')
    model.save(model_path)
    print(f"\nModel saved to: {model_path}")

    # Also save as Keras format
    keras_path = os.path.join(model_dir, 'plant_disease_model.keras')
    model.save(keras_path)
    print(f"Keras model saved to: {keras_path}")


def main():
    """
    Main training pipeline.
    """
    # Configuration
    DATA_DIR = 'data'
    MODEL_DIR = 'model'
    EPOCHS = 100
    BATCH_SIZE = 4

    # Train model
    result = train_model(DATA_DIR, epochs=EPOCHS, batch_size=BATCH_SIZE)

    if result is not None:
        model, history = result

        # Save model
        save_model(model, MODEL_DIR)

        print("\n" + "=" * 60)
        print("Training Complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Run 'python src/app.py' to start the application")
        print("2. Upload a leaf image for analysis")
        print("3. View treatment recommendations")
    else:
        print("\nTraining failed. Please check your data directory.")


if __name__ == "__main__":
    main()
