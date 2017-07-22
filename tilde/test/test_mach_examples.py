
from tilde.classification.classification_helper import do_labeled_examples_get_correctly_classified_models
from tilde.test.test_models import ModelsTestBase


class MachModelsTest(ModelsTestBase):
    def setUp(self):
        fname_settings = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.s'
        fname_background_knowledge = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.bg'
        fname_labeled_examples = 'D:\\KUL\\KUL MAI\\Masterproef\\data\\ACE-examples-data\\ace\\mach\\examples\\mach.kb'

        self.general_setup(fname_labeled_examples, fname_settings, fname_background_knowledge)

    def test_training_examples_labeled_correctly_simpleprogram(self):
        program = self.simple_program_setup()

        are_training_examples_correctly_classified = do_labeled_examples_get_correctly_classified_models(self.examples,
                                                                                                         program,
                                                                                                         self.possible_targets,
                                                                                                         self.background_knowledge)
        self.assertEqual(are_training_examples_correctly_classified, True)

    def test_training_examples_labeled_correctly_clausedb(self):

        program = self.clausedb_setup()

        are_training_examples_correctly_classified = do_labeled_examples_get_correctly_classified_models(self.examples,
                                                                                                         program,
                                                                                                         self.possible_targets,
                                                                                                         self.background_knowledge)
        self.assertEqual(are_training_examples_correctly_classified, True)

