
# 
from DependenciesChecker import DependenciesChecker
DependenciesChecker().check_dependencies()

from FeatureExtractor import FeatureExtractor
from ViewExtractor import ViewExtractor
from ArgParserController import ArgParserController
from InitialProcessController import InitialProcessController
from PreprocessingController import PreprocessingController
from ProcessingController import ProcessingController
from FinalProcessController import FinalProcessController
from APKAnalyzerView import APKAnalyzerView

class APKAnalyzerController():
    
    def start(self):
        path = ArgParserController().get_path_arg()
        dest_dir = '../apks'

        InitialProcessController().process_args(path, dest_dir)
        #
        feature_extractor = FeatureExtractor(dest_dir)
        feature_extractor.feature_extractor()
        
        #
        apks = ViewExtractor(feature_extractor.apk_dir).extract_views()
        apks = PreprocessingController().preprocessing(apks)
        
        apks = ProcessingController().processing(apks)
        FinalProcessController().clear_directory(dest_dir)
        APKAnalyzerView().show_result(apks)