import types
from abc import *
import cv2


class ObjectTracking(object):
    """Клаас ООП трекинга"""
    my_observers = list()  # Наблюдатели
    trackPoints = list()  # Точки трекинга
    tracker = None
    state = None
    instance = None

    # Конструктор
    def __init__(self):
        self.tracker = cv2.TrackerBoosting_create()
        self.state = BOOSTING()
        self.video = None
        self.tracker_type = None
        self.my_observers.append(ConcreteObserver())
        self.my_observers.append(ObserverAdapter())

    def __init__(self, video, tracker_type):
        self.tracker = cv2.TrackerBoosting_create()
        self.state = BOOSTING()
        self.video = video
        self.tracker_type = tracker_type
        self.my_observers.append(ConcreteObserver())
        self.my_observers.append(ObserverAdapter())

        if not ObjectTracking.instance:
            print("Singleton used!!!")
        else:
            print("Singleton already created:", self.getInstance())

        # Создание трекера
        if self.tracker_type == 'BOOSTING':
            self.changeState(BOOSTING)
            self.tracker = self.state.track_type
        if self.tracker_type == 'MIL':
            self.changeState(MIL)
            self.tracker = self.state.track_type
        if self.tracker_type == 'KCF':
            self.changeState(KCF)
            self.tracker = self.state.track_type
        if self.tracker_type == 'TLD':
            self.changeState(TLD)
            self.tracker = self.state.track_type
        if self.tracker_type == 'MEDIANFLOW':
            self.changeState(MEDIANFLOW)
            self.tracker = self.state.track_type
        if self.tracker_type == 'GOTURN':
            self.changeState(GOTURN)
            self.tracker = self.state.track_type
        if self.tracker_type == 'MOSSE':
            self.changeState(MOSSE)
            self.tracker = self.state.track_type
        if self.tracker_type == "CSRT":
            self.changeState(CSRT)
            self.tracker = self.state.track_type


    def changeState(self, type):
        self.state.DefineType(type)


    @classmethod
    def getInstance(cls):
        if not cls.instance:
            cls.instance = ObjectTracking()
        return cls.instance


    # Метод трекинга объекта c видео
    def TrackObjectV(self, frame, bounding_box):
        # Инициализация трекера с первым кадром и ограничительной рамкой
        ok = self.tracker.init(frame, bounding_box)

        target_lost = False

        while True:
            # Чтеник нового кадра
            ok, frame = self.video.read()
            if not ok:
                break

            # Запуск таймера
            timer = cv2.getTickCount()

            # Обновление трекера
            ok, bounding_box = self.tracker.update(frame)

            # Подсчет кадров в секунду (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Отрисовка рамки
            if ok:
                # Успешный трекинг
                p1 = (int(bounding_box[0]), int(bounding_box[1]))
                p2 = (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                self.trackPoints.append((int(bounding_box[0] + (bounding_box[2] / 2)), int(bounding_box[1] + (bounding_box[3] / 2))))
                target_lost = False
            else:
                # Ошибка трекинга
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255),2)
                if target_lost == False:
                    self.notify_observers()
                    target_lost = True

            for count in range(len(self.trackPoints)):
                if not count == 0:
                    cv2.line(frame, self.trackPoints[count], self.trackPoints[count - 1], (50, 170, 50), 3)

            if len(self.trackPoints) > 50:
                self.trackPoints.remove(self.trackPoints[0])

            # Вывод типа трекинга
            cv2.putText(frame, self.tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50),2)

            # Вывод FPS
            cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            # ВЫвод результат
            cv2.imshow("Tracking", frame)

            # ESC - выход
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                break

    # Метод отслеживания объекта с прямого видеопотока
    def TrackObject(self):
        cap = cv2.VideoCapture(0)
        ok, frame = cap.read()

        # Создание ограничительной рамки
        bounding_box = (287, 23, 86, 320)

         # Выбр другой ограничительной рамки
        bounding_box = cv2.selectROI(frame, False)

        # Инициализация трекера с первым кадром и рамкой
        ok = self.tracker.init(frame, bounding_box)

        target_lost = False

        # Выполнять до клавиши выхода
        while True:
            # Считать новый кадр
            ok, frame = cap.read()

            # Если кадр не считался, то прерываем
            if not ok:
                break

            # Старт таймера
            timer = cv2.getTickCount()

            # Обеовление трекера
            ok, bounding_box = self.tracker.update(frame)

            # Подсчет кадров в секунду (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

            # Отрисовка рамки трекинга
            if ok:
                # Удача трекинга
                p1 = (int(bounding_box[0]), int(bounding_box[1]))
                p2 = (int(bounding_box[0] + bounding_box[2]), int(bounding_box[1] + bounding_box[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

                self.trackPoints.append((int(bounding_box[0] + (bounding_box[2] / 2)), int(bounding_box[1] + (bounding_box[3] / 2))))
                target_lost = False
            else:
                # Ошибка трекинга
                cv2.putText(frame, "Tracking failure detected", (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
                if target_lost == False:
                    self.notify_observers()
                    target_lost = True

            for count in range(len(self.trackPoints)):
                if not count == 0:
                    cv2.line(frame, self.trackPoints[count], self.trackPoints[count - 1], (50, 170, 50), 3)

            if len(self.trackPoints) > 50:
                self.trackPoints.remove(self.trackPoints[0])

            # Показать имя трекера
            cv2.putText(frame, self.tracker_type + " Tracker", (50, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            # Показать FPS
            cv2.putText(frame, "FPS : " + str(int(fps)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

            # Показать результаты - вывод
            cv2.imshow("Tracking", frame)

            # ESC - выход
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                cap.release()
                cv2.destroyAllWindows()
                break

    # Метод Notify для Observer
    def notify_observers(self):
        for observ in self.my_observers:
            if isinstance(observ, Observer):
                observ.update()


class TrackType(object):
    track_type = cv2.TrackerBoosting_create()

    def DefineType(self, type):
        self.__class__ = type;
        print("State used!")


class BOOSTING(TrackType):
    track_type = cv2.TrackerBoosting_create()


class MIL(TrackType):
    track_type = cv2.TrackerMIL_create()


class KCF(TrackType):
    track_type = cv2.TrackerKCF_create()


class TLD(TrackType):
    track_type = cv2.TrackerTLD_create()


class MEDIANFLOW(TrackType):
    track_type = cv2.TrackerMedianFlow_create()


class GOTURN(TrackType):
    track_type = cv2.TrackerGOTURN_create()


class MOSSE(TrackType):
        track_type = cv2.TrackerMOSSE_create()


class CSRT(TrackType):
    track_type = cv2.TrackerCSRT_create()


class Observer(ABC):
    """Класс-паттерн Наблюдатель"""
    @abstractmethod
    def update(self):
        pass


class ConcreteObserver(Observer):
    """Конкретный Наблюдатель"""
    def update(self):
        print("Tracking failure detected")


class ObserverAdapter(Observer):
    """Наблюдатель Адаптер"""
    def update(self):
        my_observ = ThirdPartyObserver()
        my_observ.refresh()


class ThirdPartyObserver(object):
    def refresh(self):
        print("WARNING!!! Target  lost!")
