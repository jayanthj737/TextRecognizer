
"""Fully-convolutional resnet network"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List, Tuple
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Activation, Add, Conv2D, Input, Lambda, Layer
# from tensorflow.keras import backend as K
from keras.models import Model
from keras.layers import Activation, Add, Conv2D, Input, Lambda, Layer
from keras import backend as K

def residual_conv_block(input_layer: Layer,
                        kernel_sizes: List[int],
                        num_filters: List[int],
                        dilation_rates: List[int],
                        activation: str) -> Layer:
    """Function to instantiate a Residual convolutional block."""
    padding = 'same'
    x = Conv2D(num_filters[0],
               kernel_size=kernel_sizes[0],
               dilation_rate=dilation_rates[0],
               padding=padding,
               activation=activation)(input_layer)
    x = Conv2D(num_filters[1], kernel_size=kernel_sizes[1], dilation_rate=dilation_rates[1], padding=padding)(x)
    y = Conv2D(num_filters[1], kernel_size=1, dilation_rate=1, padding=padding)(input_layer)
    x = Add()([x, y])
    x = Activation(activation)(x)
    return x


def FCN(input_shape: Tuple[int, ...], output_shape: Tuple[int, ...]) -> Model:
    """Function to instantiate a fully convolutional residual network for line detection."""
    num_filters = [16] * 14
    kernel_sizes = [7] * 14
    dilation_rates = [3] * 4 + [7] * 10

    num_classes = output_shape[-1]
    input_image = Input((None, None))
    model_layer = Lambda(lambda x: K.expand_dims(x, axis=-1))(input_image)

    for i in range(0, len(num_filters), 2):
        model_layer = residual_conv_block(input_layer=model_layer,
                                          kernel_sizes=kernel_sizes[i:i+2],
                                          num_filters=num_filters[i:i+2],
                                          dilation_rates=dilation_rates[i:i+2],
                                          activation='relu')
    output = Conv2D(num_classes, kernel_size=1, dilation_rate=1, padding='same', activation='softmax')(model_layer)

    model = Model(inputs=input_image, outputs=output)
    return model

def dummy():
    num_filters = [16] * 14
    kernel_sizes = [7] * 14
    dilation_rates = [3] * 4 + [7] * 10

    num_classes = 3
    input_image = Input((None, None))
    model_layer = Lambda(lambda x: K.expand_dims(x, axis=-1))(input_image)

    for i in range(0, len(num_filters), 2):
        model_layer = residual_conv_block(input_layer=model_layer,
                                          kernel_sizes=kernel_sizes[i:i+2],
                                          num_filters=num_filters[i:i+2],
                                          dilation_rates=dilation_rates[i:i+2],
                                          activation='relu')
    output = Conv2D(num_classes, kernel_size=1, dilation_rate=1, padding='same', activation='softmax')(model_layer)

    model = Model(inputs=input_image, outputs=output)
    model.summary()

dummy()