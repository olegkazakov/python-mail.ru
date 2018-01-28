import csv

class CarBase:

  TYPE_CAR = 'car'
  TYPE_TRUCK = 'truck'
  TYPE_SPECIAL_MACHINE = 'spec_machine'

  def __init__(self, brand, photo_file_name, carrying):
    self.brand, self.photo_file_name, self.carrying = \
    brand, photo_file_name, carrying

  def get_photo_file_ext(self):
    return self.photo_file_name.split('.')[-1]

  def __repr__(self):
    return f"{self.brand}, {self.photo_file_name}, {self.carrying}"


class Car(CarBase):

  car_type = CarBase.TYPE_CAR

  def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
    super().__init__(brand, photo_file_name, carrying)
    self.passenger_seats_count = passenger_seats_count


class Truck(CarBase):

  car_type = CarBase.TYPE_TRUCK

  def __init__(self, brand, photo_file_name, carrying, body_whl):
    super().__init__(brand, photo_file_name, carrying)
    self.body_whl = body_whl
    self.body_width, self.body_height, self.body_length = \
    map(float, self.body_whl.split("x")) if self.body_whl \
    else [0.0 for _ in range(3)]

  def get_body_volume(self):
    return self.body_width*self.body_height*self.body_length


class SpecMachine(CarBase):

  car_type = CarBase.TYPE_SPECIAL_MACHINE

  def __init__(self, brand, photo_file_name, carrying, extra):
    super().__init__(brand, photo_file_name, carrying)
    self.extra = extra


def get_car_list(csv_filename):
  car_list = []
  with open(csv_filename) as csv_fd:
    reader = csv.reader(csv_fd, delimiter=';')
    next(reader)  # пропускаем заголовок
    for row in reader:
      if len(row) == 7:
        car_type, brand, passenger_seats_count, photo_file_name, \
        body_whl, carrying, extra = row

        if not brand or not photo_file_name:
          continue

        try:
          carrying = float(carrying)
          if passenger_seats_count:
            passenger_seats_count = int(passenger_seats_count)
        except ValueError:
          continue

        if car_type == CarBase.TYPE_CAR and passenger_seats_count:
          car_list.append(Car(brand, photo_file_name, carrying, passenger_seats_count))
        elif car_type == CarBase.TYPE_TRUCK:
          car_list.append(Truck(brand, photo_file_name, carrying, body_whl))
        elif car_type == CarBase.TYPE_SPECIAL_MACHINE and extra:
          car_list.append(SpecMachine(brand, photo_file_name, carrying, extra))

  return car_list
