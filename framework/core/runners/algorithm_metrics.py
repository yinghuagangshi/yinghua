import os

class AlgorithmMetrics:
    """算法指标统计类"""

    def __init__(self, label_file_path):
        self.metrics = {
            "true_positives": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "processing_time": [],
            "iou_scores": []
        }
        self.label_file_path = label_file_path
        self.ground_truth = self._load_labels()

    def _load_labels(self):
        """加载标签文件"""
        ground_truth = {}
        try:
            with open(self.label_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 6:  # filename x1 y1 x2 y2 plate_number
                        file_name = parts[0]
                        box = list(map(float, parts[1:5]))
                        plate_number = ' '.join(parts[5:])

                        if file_name not in ground_truth:
                            ground_truth[file_name] = {'boxes': [], 'plates': []}

                        ground_truth[file_name]['boxes'].append(box)
                        ground_truth[file_name]['plates'].append(plate_number)
        except FileNotFoundError:
            print(f"标签文件 {self.label_file_path} 未找到")
        return ground_truth

    def _calculate_iou(self, box1, box2):
        """计算IoU（带边界检查）"""
        if len(box1) != 4 or len(box2) != 4:
            return 0.0

        x_left = max(box1[0], box2[0])
        y_top = max(box1[1], box2[1])
        x_right = min(box1[2], box2[2])
        y_bottom = min(box1[3], box2[3])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection = (x_right - x_left) * (y_bottom - y_top)
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])

        return intersection / float(area1 + area2 - intersection)

    def update(self, content):
        """更新算法指标（优化版）"""
        if "data" not in content:
            print("警告：输入数据缺少 'data' 字段")
            return

        data = content["data"]
        pred_boxes = data.get("detected_boxes", [])
        pred_plates = data.get("plate_numbers", [])
        file_name = data.get("imageID", "")

        # 检查预测数据和真实标签
        if not file_name:
            print("警告：未提供 imageID")
            return

        if len(pred_boxes) != len(pred_plates):
            print(f"警告：预测框数量 ({len(pred_boxes)}) 和车牌数量 ({len(pred_plates)}) 不一致")
            return

        if file_name not in self.ground_truth:
            print(f"警告：{file_name} 无真实标签，跳过统计")
            return

        true_data = self.ground_truth[file_name]
        true_boxes = true_data.get("boxes", [])
        true_plates = true_data.get("plates", [])

        # 最佳匹配策略（避免重复匹配）
        matched_indices = set()
        matched = 0

        for i, pred_box in enumerate(pred_boxes):
            best_iou = 0.5  # IoU 阈值
            best_match = None

            for j, true_box in enumerate(true_boxes):
                if j in matched_indices:
                    continue

                iou = self._calculate_iou(pred_box, true_box)
                if iou >= best_iou and pred_plates[i] == true_plates[j]:
                    best_iou = iou
                    best_match = j

            if best_match is not None:
                matched_indices.add(best_match)
                matched += 1
                self.metrics["iou_scores"].append(best_iou)

        # 更新指标
        self.metrics["true_positives"] += matched
        self.metrics["false_positives"] += len(pred_boxes) - matched
        self.metrics["false_negatives"] += len(true_boxes) - matched

    def get_summary(self):
        """获取算法指标摘要"""
        tp = self.metrics["true_positives"]
        fp = self.metrics["false_positives"]
        fn = self.metrics["false_negatives"]

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "avg_iou": sum(self.metrics["iou_scores"]) / len(self.metrics["iou_scores"]) if self.metrics["iou_scores"] else 0,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn
        }